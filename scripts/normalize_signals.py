#!/usr/bin/env python3
"""Normalize raw API signals into candidate startup signals."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib
import re
import sys
import urllib.parse
from typing import Any


ROOT = pathlib.Path(__file__).resolve().parents[1]


AI_TERMS = ("ai", "artificial intelligence", "llm", "agent", "copilot", "automation", "machine learning")
REGION_HINTS = {
    "Silicon Valley": ("san francisco", "silicon valley", "palo alto", "menlo park", "mountain view", "bay area"),
    "New York": ("new york", "nyc", "brooklyn", "manhattan"),
    "Singapore": ("singapore",),
    "Hong Kong": ("hong kong", "hk "),
}


def slug_text(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def domain_of(url: str) -> str:
    try:
        return urllib.parse.urlparse(url).netloc.lower().removeprefix("www.")
    except Exception:
        return ""


def infer_region(text: str) -> str:
    lowered = f" {text.lower()} "
    for region, hints in REGION_HINTS.items():
        if any(hint in lowered for hint in hints):
            return region
    return "Unclear"


def infer_ai_core(text: str) -> str:
    lowered = text.lower()
    return "yes" if any(term in lowered for term in AI_TERMS) else "unclear"


def infer_signal_type(provider: str, text: str) -> str:
    lowered = text.lower()
    if provider == "github":
        return "open-source traction"
    if "funding" in lowered or "raises" in lowered or "raised" in lowered:
        return "funding"
    if "launch" in lowered or "introduces" in lowered or "announces" in lowered:
        return "launch"
    if "partner" in lowered or "partnership" in lowered:
        return "partnership"
    return "news signal"


def candidate_from_signal(signal: dict[str, Any]) -> dict[str, Any]:
    title = signal.get("title") or "Unknown"
    snippet = signal.get("snippet") or ""
    provider = signal.get("provider") or signal.get("source") or "unknown"
    text = f"{title} {snippet}"
    url = signal.get("url") or ""
    return {
        "company": title,
        "region": infer_region(text),
        "source_date": signal.get("published_at") or "",
        "signal_type": infer_signal_type(provider, text),
        "one_sentence_signal": snippet or title,
        "ai_is_core": infer_ai_core(text),
        "stage": "",
        "sector": "",
        "customer": "",
        "business_model": "",
        "founder_team_signal": "",
        "traction_signal": "",
        "scoring_evidence": {
            "freshness": f"Source date: {signal.get('published_at') or 'unknown'}",
            "ai_centrality": "Inferred from title/snippet; verify before scoring high.",
            "customer_pain": "",
            "business_model": "",
            "founder_team_fit": "",
            "traction_distribution": provider,
            "defensibility": "",
            "market_timing": "",
            "personal_lens_fit": "",
        },
        "source_links": [url] if url else [],
        "raw_sources": [signal],
    }


def dedupe(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: dict[str, dict[str, Any]] = {}
    for candidate in candidates:
        domain = domain_of((candidate.get("source_links") or [""])[0])
        key = domain or slug_text(candidate.get("company", ""))
        if key in seen:
            existing = seen[key]
            existing["source_links"] = sorted(set(existing.get("source_links", []) + candidate.get("source_links", [])))
            existing["raw_sources"].extend(candidate.get("raw_sources", []))
            if existing.get("region") == "Unclear" and candidate.get("region") != "Unclear":
                existing["region"] = candidate["region"]
        else:
            seen[key] = candidate
    return list(seen.values())


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize raw signals into candidate signals.")
    parser.add_argument("--in", dest="input_path", default=str(ROOT / "work" / "raw_signals.json"))
    parser.add_argument("--out", default=str(ROOT / "work" / "candidate_signals.json"))
    args = parser.parse_args()

    input_path = pathlib.Path(args.input_path)
    if not input_path.exists():
        print(f"Input file not found: {input_path}", file=sys.stderr)
        return 2

    raw_payload = json.loads(input_path.read_text(encoding="utf-8"))
    raw_signals = raw_payload.get("signals", [])
    candidates = dedupe([candidate_from_signal(signal) for signal in raw_signals])

    payload = {
        "normalized_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "raw_signal_count": len(raw_signals),
        "candidate_count": len(candidates),
        "candidates": candidates,
    }
    out_path = pathlib.Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(candidates)} candidate signals to {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
