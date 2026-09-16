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


AI_TERMS = (
    "ai",
    "artificial intelligence",
    "generative ai",
    "llm",
    "large language model",
    "agentic",
    "agent",
    "copilot",
    "rag",
    "automation",
    "machine learning",
    "computer vision",
    "voice agent",
)
PRODUCT_TERMS = (
    "platform",
    "product",
    "saas",
    "enterprise",
    "customer",
    "workflow",
    "automation",
    "agent",
    "copilot",
    "assistant",
    "dashboard",
    "api",
    "production",
    "beta",
    "waitlist",
    "founder",
    "startup",
    "inc",
    "labs",
    "hq",
)
SIGNAL_TERMS = (
    "funding",
    "raises",
    "raised",
    "launch",
    "launched",
    "introduces",
    "announces",
    "partnership",
    "customer",
    "pilot",
    "open source",
    "released",
)
NOISE_TERMS = (
    "starter",
    "starter kit",
    "starter-template",
    "starter-project",
    "template",
    "boilerplate",
    "tutorial",
    "course",
    "workshop",
    "hackathon",
    "homework",
    "assignment",
    "clone",
    "docs",
    "documentation",
    "example",
    "sample",
    "awesome",
    "awesome list",
    "replication package",
    "case study",
    "working draft",
    "minimal laravel",
)
SECTOR_HINTS = {
    "AI Agent": ("agent", "agentic", "copilot", "assistant", "workflow automation"),
    "Vertical AI": ("enterprise", "industry", "vertical", "industrial", "maintenance", "forensics", "legal", "finance"),
    "Healthcare": ("health", "clinical", "medical", "bioinformatics", "biotech", "patient", "care", "wellness"),
    "Sports": ("sport", "sports", "fitness", "athlete"),
    "Career": ("career", "recruiting", "resume", "job", "hiring", "professional"),
    "Developer Tools": ("developer", "code", "coding", "devtools", "langchain", "api", "sdk"),
}
REGION_HINTS = {
    "Silicon Valley": ("san francisco", "silicon valley", "palo alto", "menlo park", "mountain view", "bay area"),
    "New York": ("new york", "nyc", "brooklyn", "manhattan"),
    "Singapore": ("singapore",),
    "Hong Kong": ("hong kong", "hk "),
}


def slug_text(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def keyword_hits(text: str, terms: tuple[str, ...]) -> list[str]:
    normalized = f" {slug_text(text)} "
    hits = []
    for term in terms:
        normalized_term = slug_text(term)
        if not normalized_term:
            continue
        pattern = rf"(?<![a-z0-9]){re.escape(normalized_term)}(?![a-z0-9])"
        if re.search(pattern, normalized):
            hits.append(term)
    return hits


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
    return "yes" if keyword_hits(text, AI_TERMS) else "unclear"


def infer_sector(text: str) -> str:
    matches = [sector for sector, hints in SECTOR_HINTS.items() if keyword_hits(text, hints)]
    return ", ".join(matches[:2])


def infer_customer(text: str) -> str:
    lowered = text.lower()
    if keyword_hits(lowered, ("developer", "code", "coding", "devtools", "api", "sdk")):
        return "Developers / technical teams"
    if keyword_hits(lowered, ("enterprise", "production", "workflow", "industrial", "maintenance")):
        return "Enterprise or operational teams"
    if keyword_hits(lowered, ("health", "medical", "clinical", "patient", "wellness")):
        return "Healthcare or wellness users"
    if keyword_hits(lowered, ("career", "job", "hiring", "resume", "recruiting")):
        return "Career or hiring users"
    return ""


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


def quality_assessment(signal: dict[str, Any], visible_text: str) -> dict[str, Any]:
    metadata = signal.get("metadata") or {}
    provider = signal.get("provider") or signal.get("source") or "unknown"
    query_text = str(signal.get("query") or "")
    combined_text = f"{visible_text} {query_text} {' '.join(metadata.get('topics') or [])} {metadata.get('owner') or ''}"
    ai_hits = keyword_hits(visible_text, AI_TERMS)
    query_ai_hits = keyword_hits(query_text, AI_TERMS)
    product_hits = keyword_hits(combined_text, PRODUCT_TERMS)
    signal_hits = keyword_hits(combined_text, SIGNAL_TERMS)
    noise_hits = keyword_hits(combined_text, NOISE_TERMS)
    company_entity_hits = keyword_hits(f"{signal.get('title') or ''} {metadata.get('owner') or ''}", ("inc", "corp"))
    sector_hits = [sector for sector, hints in SECTOR_HINTS.items() if keyword_hits(combined_text, hints)]

    score = 0
    reasons: list[str] = []
    deductions: list[str] = []

    if ai_hits:
        score += 3
        reasons.append(f"AI terms visible: {', '.join(ai_hits[:3])}")
    elif query_ai_hits:
        score += 1
        reasons.append("AI relevance comes from the source query; verify manually")
    else:
        deductions.append("No clear AI term in title, snippet, topics, or query")

    if product_hits:
        score += min(3, 1 + len(product_hits) // 3)
        reasons.append(f"Product/startup language: {', '.join(product_hits[:4])}")

    if signal_hits:
        score += 2
        reasons.append(f"Current signal language: {', '.join(signal_hits[:3])}")

    if sector_hits:
        score += min(2, len(sector_hits))
        reasons.append(f"Lens sector match: {', '.join(sector_hits[:2])}")

    if company_entity_hits:
        score += 1
        reasons.append(f"Company-like entity hint: {', '.join(company_entity_hits[:2])}")

    if infer_region(combined_text) != "Unclear":
        score += 1
        reasons.append("Target-region hint present")

    if provider in {"gdelt", "newsapi", "product_hunt"}:
        score += 2
        reasons.append(f"Source type is useful for startup discovery: {provider}")

    if provider == "github":
        stars = int(metadata.get("stars") or 0)
        owner_type = str(metadata.get("owner_type") or "")
        owner = str(metadata.get("owner") or "")
        if stars >= 50:
            score += 4
            reasons.append("GitHub traction: 50+ stars")
        elif stars >= 10:
            score += 3
            reasons.append("GitHub traction: 10+ stars")
        elif stars >= 3:
            score += 2
            reasons.append("GitHub traction: 3+ stars")
        elif stars >= 1:
            score += 1
            reasons.append("GitHub traction: at least 1 star")
        if owner_type.lower() == "organization":
            score += 2
            reasons.append("GitHub owner is an organization")
        if keyword_hits(owner, ("inc", "labs", "ai", "hq", "tech")):
            score += 1
            reasons.append("Owner name looks company-like")
        if stars == 0 and owner_type.lower() != "organization" and not signal_hits:
            score -= 1
            deductions.append("No GitHub traction and no current product signal")

    if noise_hits:
        penalty = min(6, 3 + len(noise_hits))
        score -= penalty
        deductions.append(f"Likely non-startup noise: {', '.join(noise_hits[:4])}")

    return {
        "score": score,
        "reasons": reasons,
        "deductions": deductions,
        "noise_hits": noise_hits,
        "ai_hits": ai_hits or query_ai_hits,
    }


def candidate_from_signal(signal: dict[str, Any]) -> dict[str, Any]:
    title = signal.get("title") or "Unknown"
    snippet = signal.get("snippet") or ""
    provider = signal.get("provider") or signal.get("source") or "unknown"
    metadata = signal.get("metadata") or {}
    topic_text = " ".join(metadata.get("topics") or [])
    text = f"{title} {snippet} {topic_text}"
    url = signal.get("url") or ""
    quality = quality_assessment(signal, text)
    sector = infer_sector(text)
    customer = infer_customer(text)
    is_repo_only = provider == "github"
    verification_status = "project_signal_needs_verification" if is_repo_only else "needs_verification"
    return {
        "company": title,
        "verification_status": verification_status,
        "eligible_for_company_briefing": False,
        "verification_sources": [],
        "region": infer_region(text),
        "source_date": signal.get("published_at") or "",
        "signal_type": infer_signal_type(provider, text),
        "one_sentence_signal": snippet or title,
        "ai_is_core": infer_ai_core(text),
        "stage": "",
        "sector": sector,
        "customer": customer,
        "business_model": "",
        "founder_team_signal": "",
        "traction_signal": f"{provider}; stars={metadata.get('stars')}" if provider == "github" else provider,
        "provider": provider,
        "candidate_quality_score": quality["score"],
        "candidate_quality_reasons": quality["reasons"],
        "candidate_quality_deductions": quality["deductions"],
        "source_confidence": "Medium" if quality["score"] >= 7 else "Low",
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
        key = dedupe_key(candidate)
        if key in seen:
            existing = seen[key]
            existing["source_links"] = sorted(set(existing.get("source_links", []) + candidate.get("source_links", [])))
            existing["raw_sources"].extend(candidate.get("raw_sources", []))
            if candidate.get("candidate_quality_score", 0) > existing.get("candidate_quality_score", 0):
                existing["candidate_quality_score"] = candidate["candidate_quality_score"]
                existing["candidate_quality_reasons"] = candidate.get("candidate_quality_reasons", [])
                existing["candidate_quality_deductions"] = candidate.get("candidate_quality_deductions", [])
            if existing.get("region") == "Unclear" and candidate.get("region") != "Unclear":
                existing["region"] = candidate["region"]
        else:
            seen[key] = candidate
    return list(seen.values())


def dedupe_key(candidate: dict[str, Any]) -> str:
    url = (candidate.get("source_links") or [""])[0]
    parsed = urllib.parse.urlparse(url)
    domain = parsed.netloc.lower().removeprefix("www.")
    if domain == "github.com":
        parts = [part for part in parsed.path.split("/") if part]
        if len(parts) >= 2:
            return f"github.com/{parts[0].lower()}/{parts[1].lower()}"
    return domain or slug_text(candidate.get("company", ""))


def should_keep(candidate: dict[str, Any], min_quality_score: int) -> bool:
    if candidate.get("ai_is_core") == "unclear" and candidate.get("candidate_quality_score", 0) < min_quality_score + 2:
        return False
    if candidate.get("candidate_quality_score", 0) < min_quality_score:
        return False
    if candidate.get("provider") == "github":
        raw_source = (candidate.get("raw_sources") or [{}])[0]
        metadata = raw_source.get("metadata") or {}
        stars = int(metadata.get("stars") or 0)
        owner_type = str(metadata.get("owner_type") or "")
        companyish_name = bool(keyword_hits(candidate.get("company", ""), ("inc", "corp", "labs", "hq", "ai")))
        sector = candidate.get("sector") or ""
        focused_vertical = any(label in sector for label in ("Vertical AI", "Healthcare", "Sports", "Career"))
        deductions = " ".join(candidate.get("candidate_quality_deductions") or [])
        if "Likely non-startup noise" in deductions and stars < 3 and owner_type.lower() != "organization":
            return False
        if stars == 0 and owner_type.lower() != "organization" and not companyish_name and not focused_vertical:
            return False
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize raw signals into candidate signals.")
    parser.add_argument("--in", dest="input_path", default=str(ROOT / "work" / "raw_signals.json"))
    parser.add_argument("--out", default=str(ROOT / "work" / "candidate_signals.json"))
    parser.add_argument("--min-quality-score", type=int, default=5)
    parser.add_argument("--max-candidates", type=int, default=30)
    args = parser.parse_args()

    input_path = pathlib.Path(args.input_path)
    if not input_path.exists():
        print(f"Input file not found: {input_path}", file=sys.stderr)
        return 2

    raw_payload = json.loads(input_path.read_text(encoding="utf-8"))
    raw_signals = raw_payload.get("signals", [])
    all_candidates = dedupe([candidate_from_signal(signal) for signal in raw_signals])
    candidates = [candidate for candidate in all_candidates if should_keep(candidate, args.min_quality_score)]
    candidates.sort(key=lambda item: item.get("candidate_quality_score", 0), reverse=True)
    candidates = candidates[: args.max_candidates]

    payload = {
        "normalized_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "raw_signal_count": len(raw_signals),
        "min_quality_score": args.min_quality_score,
        "rejected_count": max(0, len(all_candidates) - len(candidates)),
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
