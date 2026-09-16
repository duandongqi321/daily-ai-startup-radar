#!/usr/bin/env python3
"""Fetch raw startup signals from configured sources.

The script uses only Python standard library modules. Sources without required
credentials are skipped cleanly. Use --dry-run to inspect the planned fetches.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import pathlib
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any


ROOT = pathlib.Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "config" / "sources.yaml"
EXAMPLE_CONFIG = ROOT / "config" / "sources.example.yaml"


def load_dotenv(path: pathlib.Path) -> None:
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def parse_simple_sources_yaml(path: pathlib.Path) -> dict[str, Any]:
    """Parse the constrained YAML shape used by config/sources.example.yaml."""
    data: dict[str, Any] = {"sources": []}
    current_source: dict[str, Any] | None = None
    in_sources = False
    in_queries = False
    source_queries = False

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        line = raw_line.strip()

        if line == "sources:":
            in_sources = True
            in_queries = False
            continue
        if line == "queries:" and not in_sources:
            in_queries = True
            data.setdefault("queries", [])
            continue
        if in_queries and line.startswith("- "):
            data["queries"].append(unquote_yaml_value(line[2:]))
            continue

        if in_sources and indent == 2 and line.startswith("- "):
            if current_source:
                data["sources"].append(current_source)
            current_source = {}
            source_queries = False
            key, value = line[2:].split(":", 1)
            current_source[key.strip()] = parse_scalar(value.strip())
            continue

        if in_sources and current_source is not None and indent == 4:
            if line == "queries:":
                current_source["queries"] = []
                source_queries = True
                continue
            if ":" in line:
                key, value = line.split(":", 1)
                current_source[key.strip()] = parse_scalar(value.strip())
                source_queries = False
            continue

        if in_sources and current_source is not None and source_queries and indent == 6 and line.startswith("- "):
            current_source.setdefault("queries", []).append(unquote_yaml_value(line[2:]))

    if current_source:
        data["sources"].append(current_source)
    return data


def parse_scalar(value: str) -> Any:
    value = unquote_yaml_value(value)
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    if re.fullmatch(r"\d+", value):
        return int(value)
    return value


def unquote_yaml_value(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def request_json(url: str, headers: dict[str, str] | None = None, data: bytes | None = None) -> Any:
    req = urllib.request.Request(url, headers=headers or {}, data=data)
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def iso_since(hours: int) -> str:
    return (dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=hours)).replace(microsecond=0).isoformat()


def date_since(hours: int) -> str:
    return (dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=hours)).date().isoformat()


def expand_query(query: str, lookback_hours: int) -> str:
    return query.replace("<since-date>", date_since(lookback_hours))


def fetch_github(source: dict[str, Any], lookback_hours: int) -> list[dict[str, Any]]:
    token = os.environ.get(str(source.get("auth_env") or ""))
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    signals = []
    for query in source.get("queries", []):
        q = expand_query(query, lookback_hours)
        params = urllib.parse.urlencode({"q": q, "sort": "updated", "order": "desc", "per_page": source.get("max_results", 20)})
        data = request_json(f"https://api.github.com/search/repositories?{params}", headers=headers)
        for item in data.get("items", []):
            signals.append(
                {
                    "source": source["name"],
                    "provider": "github",
                    "query": q,
                    "title": item.get("full_name"),
                    "url": item.get("html_url"),
                    "published_at": item.get("created_at") or item.get("updated_at"),
                    "snippet": item.get("description") or "",
                    "metadata": {
                        "stars": item.get("stargazers_count"),
                        "forks": item.get("forks_count"),
                        "language": item.get("language"),
                        "topics": item.get("topics", []),
                    },
                }
            )
    return signals


def fetch_gdelt(source: dict[str, Any], lookback_hours: int) -> list[dict[str, Any]]:
    signals = []
    for query in source.get("queries", []):
        expanded = expand_query(query, lookback_hours)
        params = urllib.parse.urlencode(
            {
                "query": expanded,
                "mode": "ArtList",
                "format": "json",
                "maxrecords": source.get("max_results", 25),
                "sort": "datedesc",
            }
        )
        data = request_json(f"https://api.gdeltproject.org/api/v2/doc/doc?{params}")
        for article in data.get("articles", []):
            signals.append(
                {
                    "source": source["name"],
                    "provider": "gdelt",
                    "query": expanded,
                    "title": article.get("title"),
                    "url": article.get("url"),
                    "published_at": article.get("seendate"),
                    "snippet": article.get("sourceCommonName") or "",
                    "metadata": {"domain": article.get("domain"), "language": article.get("language")},
                }
            )
    return signals


def fetch_newsapi(source: dict[str, Any], lookback_hours: int) -> list[dict[str, Any]]:
    key = os.environ.get(str(source.get("auth_env") or ""))
    if not key:
        return []
    signals = []
    for query in source.get("queries", []):
        params = urllib.parse.urlencode(
            {
                "q": expand_query(query, lookback_hours),
                "from": date_since(lookback_hours),
                "sortBy": "publishedAt",
                "pageSize": source.get("max_results", 25),
                "apiKey": key,
            }
        )
        data = request_json(f"https://newsapi.org/v2/everything?{params}")
        for article in data.get("articles", []):
            signals.append(
                {
                    "source": source["name"],
                    "provider": "newsapi",
                    "query": query,
                    "title": article.get("title"),
                    "url": article.get("url"),
                    "published_at": article.get("publishedAt"),
                    "snippet": article.get("description") or "",
                    "metadata": {"source": (article.get("source") or {}).get("name")},
                }
            )
    return signals


def fetch_product_hunt(source: dict[str, Any], lookback_hours: int) -> list[dict[str, Any]]:
    token = os.environ.get(str(source.get("auth_env") or ""))
    if not token:
        return []
    query = """
      query FetchPosts($first: Int!, $postedAfter: DateTime) {
        posts(first: $first, postedAfter: $postedAfter) {
          edges {
            node {
              name
              tagline
              url
              website
              createdAt
              votesCount
            }
          }
        }
      }
    """
    payload = json.dumps(
        {"query": query, "variables": {"first": int(source.get("max_results", 20)), "postedAfter": iso_since(lookback_hours)}}
    ).encode("utf-8")
    data = request_json(
        "https://api.producthunt.com/v2/api/graphql",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        data=payload,
    )
    signals = []
    for edge in (((data.get("data") or {}).get("posts") or {}).get("edges") or []):
        node = edge.get("node") or {}
        text = f"{node.get('name', '')} {node.get('tagline', '')}".lower()
        if source.get("queries") and not any(str(q).lower() in text for q in source.get("queries", [])):
            continue
        signals.append(
            {
                "source": source["name"],
                "provider": "product_hunt",
                "query": ",".join(source.get("queries", [])),
                "title": node.get("name"),
                "url": node.get("website") or node.get("url"),
                "published_at": node.get("createdAt"),
                "snippet": node.get("tagline") or "",
                "metadata": {"product_hunt_url": node.get("url"), "votes": node.get("votesCount")},
            }
        )
    return signals


def fetch_source(source: dict[str, Any], lookback_hours: int) -> tuple[list[dict[str, Any]], str | None]:
    if not source.get("enabled", False):
        return [], "disabled"
    auth_env = str(source.get("auth_env") or "")
    if auth_env and not os.environ.get(auth_env):
        return [], f"missing credential {auth_env}"
    provider = source.get("provider")
    try:
        if provider == "github":
            return fetch_github(source, lookback_hours), None
        if provider == "gdelt":
            return fetch_gdelt(source, lookback_hours), None
        if provider == "newsapi":
            return fetch_newsapi(source, lookback_hours), None
        if provider == "product_hunt":
            return fetch_product_hunt(source, lookback_hours), None
        return [], f"provider {provider} is not implemented in this local helper"
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, json.JSONDecodeError) as exc:
        return [], f"{type(exc).__name__}: {exc}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch raw AI startup signals.")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG if DEFAULT_CONFIG.exists() else EXAMPLE_CONFIG))
    parser.add_argument("--out", default=str(ROOT / "work" / "raw_signals.json"))
    parser.add_argument("--lookback-hours", type=int, default=24)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    load_dotenv(ROOT / ".env")
    config_path = pathlib.Path(args.config)
    config = parse_simple_sources_yaml(config_path)

    plan = []
    signals: list[dict[str, Any]] = []
    skipped: list[dict[str, str]] = []
    for source in config.get("sources", []):
        plan.append({"name": source.get("name"), "provider": source.get("provider"), "enabled": source.get("enabled")})
        if args.dry_run:
            continue
        results, reason = fetch_source(source, args.lookback_hours)
        if reason:
            skipped.append({"source": str(source.get("name")), "reason": reason})
        signals.extend(results)

    if args.dry_run:
        print(json.dumps({"config": str(config_path), "lookback_hours": args.lookback_hours, "plan": plan}, ensure_ascii=False, indent=2))
        return 0

    out_path = pathlib.Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "fetched_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "config": str(config_path),
        "lookback_hours": args.lookback_hours,
        "raw_signal_count": len(signals),
        "skipped_sources": skipped,
        "signals": signals,
    }
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(signals)} raw signals to {out_path}")
    if skipped:
        print("Skipped sources:")
        for item in skipped:
            print(f"- {item['source']}: {item['reason']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
