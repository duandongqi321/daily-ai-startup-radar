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
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any


ROOT = pathlib.Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "config" / "sources.yaml"
EXAMPLE_CONFIG = ROOT / "config" / "sources.example.yaml"
SSL_CONTEXT: ssl.SSLContext | None = None
PRODUCT_HUNT_DEFAULT_KEYWORDS = (
    "ai",
    "artificial intelligence",
    "agent",
    "agentic",
    "automation",
    "chatbot",
    "copilot",
    "developer tools",
    "devtools",
    "llm",
    "machine learning",
    "no-code",
    "productivity",
    "rag",
    "workflow",
)


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
    in_defaults = False
    in_queries = False
    source_queries = False

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        line = raw_line.strip()

        if line == "sources:":
            in_sources = True
            in_defaults = False
            in_queries = False
            continue
        if line == "defaults:":
            in_defaults = True
            in_sources = False
            in_queries = False
            data.setdefault("defaults", {})
            continue
        if line == "queries:" and not in_sources:
            in_queries = True
            in_defaults = False
            data.setdefault("queries", [])
            continue
        if in_queries and line.startswith("- "):
            data["queries"].append(unquote_yaml_value(line[2:]))
            continue
        if in_defaults and indent == 2 and ":" in line:
            key, value = line.split(":", 1)
            data.setdefault("defaults", {})[key.strip()] = parse_scalar(value.strip())
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


def build_ssl_context(allow_insecure_ssl: bool = False) -> ssl.SSLContext | None:
    if allow_insecure_ssl:
        return ssl._create_unverified_context()
    try:
        import certifi  # type: ignore

        return ssl.create_default_context(cafile=certifi.where())
    except Exception:
        return None


def request_json(url: str, headers: dict[str, str] | None = None, data: bytes | None = None) -> Any:
    req = urllib.request.Request(url, headers=headers or {}, data=data)
    open_kwargs: dict[str, Any] = {"timeout": 30}
    if SSL_CONTEXT is not None:
        open_kwargs["context"] = SSL_CONTEXT
    with urllib.request.urlopen(req, **open_kwargs) as response:
        return json.loads(response.read().decode("utf-8"))


def iso_since(hours: int) -> str:
    return (dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=hours)).replace(microsecond=0).isoformat()


def date_since(hours: int) -> str:
    return (dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=hours)).date().isoformat()


def expand_query(query: str, lookback_hours: int) -> str:
    return query.replace("<since-date>", date_since(lookback_hours))


def keyword_matches(text: str, keywords: list[str] | tuple[str, ...]) -> list[str]:
    normalized = f" {re.sub(r'[^a-z0-9]+', ' ', text.lower()).strip()} "
    matches = []
    for keyword in keywords:
        normalized_keyword = re.sub(r"[^a-z0-9]+", " ", str(keyword).lower()).strip()
        if not normalized_keyword:
            continue
        pattern = rf"(?<![a-z0-9]){re.escape(normalized_keyword)}(?![a-z0-9])"
        if re.search(pattern, normalized):
            matches.append(str(keyword))
    return matches


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
                        "owner": ((item.get("owner") or {}).get("login")),
                        "owner_type": ((item.get("owner") or {}).get("type")),
                        "created_at": item.get("created_at"),
                        "updated_at": item.get("updated_at"),
                        "pushed_at": item.get("pushed_at"),
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
                "language": source.get("language", "en"),
                "searchIn": source.get("search_in", "title,description"),
                "sortBy": "publishedAt",
                "pageSize": source.get("max_results", 25),
            }
        )
        data = request_json(f"https://newsapi.org/v2/everything?{params}", headers={"X-Api-Key": key})
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
      query FetchPosts($first: Int!, $after: String, $postedAfter: DateTime) {
        posts(first: $first, after: $after, postedAfter: $postedAfter) {
          pageInfo {
            hasNextPage
            endCursor
          }
          edges {
            node {
              name
              tagline
              description
              url
              website
              createdAt
              votesCount
              topics {
                edges {
                  node {
                    name
                    slug
                  }
                }
              }
            }
          }
        }
      }
    """
    max_results = int(source.get("max_results", 100))
    keywords = [str(query) for query in source.get("queries", [])] or list(PRODUCT_HUNT_DEFAULT_KEYWORDS)
    signals = []
    fetched = 0
    after: str | None = None
    posted_after = iso_since(lookback_hours)

    while fetched < max_results:
        first = min(20, max_results - fetched)
        payload = json.dumps(
            {"query": query, "variables": {"first": first, "after": after, "postedAfter": posted_after}}
        ).encode("utf-8")
        data = request_json(
            "https://api.producthunt.com/v2/api/graphql",
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            data=payload,
        )
        if data.get("errors"):
            message = "; ".join(str(error.get("message") or error) for error in data.get("errors", []))
            raise RuntimeError(f"Product Hunt GraphQL error: {message}")

        posts = (data.get("data") or {}).get("posts") or {}
        edges = posts.get("edges") or []
        page_info = posts.get("pageInfo") or {}
        fetched += len(edges)

        for edge in edges:
            node = edge.get("node") or {}
            topic_edges = (((node.get("topics") or {}).get("edges")) or [])
            topic_names = [str(((edge.get("node") or {}).get("name")) or "") for edge in topic_edges]
            topic_slugs = [str(((edge.get("node") or {}).get("slug")) or "") for edge in topic_edges]
            text = " ".join(
                [
                    str(node.get("name") or ""),
                    str(node.get("tagline") or ""),
                    str(node.get("description") or ""),
                    " ".join(topic_names),
                    " ".join(topic_slugs),
                ]
            )
            matches = keyword_matches(text, keywords)
            if not matches:
                continue
            tagline = str(node.get("tagline") or "").strip()
            description = str(node.get("description") or "").strip()
            snippet = tagline or description
            signals.append(
                {
                    "source": source["name"],
                    "provider": "product_hunt",
                    "query": ",".join(matches[:6]),
                    "title": node.get("name"),
                    "url": node.get("website") or node.get("url"),
                    "published_at": node.get("createdAt"),
                    "snippet": snippet,
                    "metadata": {
                        "description": description,
                        "matched_keywords": matches,
                        "product_hunt_url": node.get("url"),
                        "topics": [topic for topic in topic_names if topic],
                        "topic_slugs": [slug for slug in topic_slugs if slug],
                        "votes": node.get("votesCount"),
                        "website": node.get("website"),
                    },
                }
            )

        if not page_info.get("hasNextPage") or not page_info.get("endCursor") or not edges:
            break
        after = str(page_info.get("endCursor"))

    return signals


def fetch_source(source: dict[str, Any], lookback_hours: int) -> tuple[list[dict[str, Any]], str | None]:
    if not source.get("enabled", False):
        return [], "disabled"
    auth_env = str(source.get("auth_env") or "")
    requires_auth = bool(source.get("requires_auth", bool(auth_env)))
    if auth_env and requires_auth and not os.environ.get(auth_env):
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
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, json.JSONDecodeError, RuntimeError) as exc:
        return [], f"{type(exc).__name__}: {exc}"


def main() -> int:
    global SSL_CONTEXT

    parser = argparse.ArgumentParser(description="Fetch raw AI startup signals.")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG if DEFAULT_CONFIG.exists() else EXAMPLE_CONFIG))
    parser.add_argument("--out", default=str(ROOT / "work" / "raw_signals.json"))
    parser.add_argument("--lookback-hours", type=int, default=None)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--allow-insecure-ssl",
        action="store_true",
        help="Last-resort local testing option for machines with broken Python certificate setup.",
    )
    args = parser.parse_args()

    SSL_CONTEXT = build_ssl_context(args.allow_insecure_ssl)
    load_dotenv(ROOT / ".env")
    config_path = pathlib.Path(args.config)
    config = parse_simple_sources_yaml(config_path)
    defaults = config.get("defaults", {}) if isinstance(config.get("defaults", {}), dict) else {}
    lookback_hours = int(args.lookback_hours or defaults.get("lookback_hours") or 720)

    plan = []
    signals: list[dict[str, Any]] = []
    skipped: list[dict[str, str]] = []
    for source in config.get("sources", []):
        plan.append({"name": source.get("name"), "provider": source.get("provider"), "enabled": source.get("enabled")})
        if args.dry_run:
            continue
        results, reason = fetch_source(source, lookback_hours)
        if reason:
            skipped.append({"source": str(source.get("name")), "reason": reason})
        signals.extend(results)

    if args.dry_run:
        print(json.dumps({"config": str(config_path), "lookback_hours": lookback_hours, "plan": plan}, ensure_ascii=False, indent=2))
        return 0

    out_path = pathlib.Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "fetched_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "config": str(config_path),
        "lookback_hours": lookback_hours,
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
