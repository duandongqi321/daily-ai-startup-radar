# Signal Pipeline

Use this reference when turning API results into a Daily AI Startup Radar briefing.

## Pipeline Overview

```text
source config
→ fetch raw signals
→ normalize fields
→ deduplicate companies/events
→ filter by recency, region, AI relevance, company verification, and source quality
→ enrich with supporting sources
→ score with the rubric
→ select 5-7 companies
→ generate HTML briefing
```

## Step 1: Fetch Raw Signals

Use `scripts/fetch_signals.py` when a local execution environment is available.

Expected inputs:

- `config/sources.yaml`, or `config/sources.example.yaml` as a fallback
- environment variables from `.env`
- lookback window

Expected output:

```text
work/raw_signals.json
```

Useful commands:

```text
python3 scripts/fetch_signals.py --dry-run
python3 scripts/fetch_signals.py
python3 scripts/fetch_signals.py --allow-insecure-ssl
```

Use `--allow-insecure-ssl` only as a local testing fallback when macOS/Python certificate setup blocks public HTTPS requests.

Raw signals should include:

- source
- source query
- title or company name
- URL
- published or created date
- snippet or description
- region hints
- source-specific metadata

GitHub repositories are discovery signals only. A GitHub result must be enriched with a company/product source before it can become a ranked company.

## Step 2: Normalize Signals

Use `scripts/normalize_signals.py` to transform raw source-specific results into a shared candidate format.

Expected output:

```text
work/candidate_signals.json
```

Candidate fields:

```json
{
  "company": "",
  "verification_status": "verified_company/project_signal_needs_verification",
  "eligible_for_company_briefing": false,
  "verification_sources": [],
  "region": "",
  "source_date": "",
  "signal_type": "",
  "one_sentence_signal": "",
  "ai_is_core": "yes/no/unclear",
  "stage": "",
  "sector": "",
  "customer": "",
  "business_model": "",
  "founder_team_signal": "",
  "traction_signal": "",
  "candidate_quality_score": 0,
  "candidate_quality_reasons": [],
  "candidate_quality_deductions": [],
  "source_confidence": "Low/Medium/High",
  "scoring_evidence": {
    "freshness": "",
    "ai_centrality": "",
    "customer_pain": "",
    "business_model": "",
    "founder_team_fit": "",
    "traction_distribution": "",
    "defensibility": "",
    "market_timing": "",
    "personal_lens_fit": ""
  },
  "source_links": []
}
```

## Step 3: Deduplicate

Deduplicate by:

- normalized company name
- domain
- identical URL
- highly similar title
- same company plus same signal type

Keep all source links when merging duplicates.

## Step 4: Filter

Prefer signals that satisfy:

- within the configured 30-day lookback window
- relevant to at least one target region or globally relevant with a clear region basis
- AI is central or plausibly central
- has product, company, launch, funding, customer, traction, or vertical workflow evidence
- has external company verification beyond a repo-only signal
- source is credible enough to cite
- enough evidence exists for dimension-level scoring

Reject or mark Low confidence:

- stale reposts
- vague listicles
- repo-only results that cannot be connected to a real company, product page, founder profile, launch, or credible article
- templates, starter kits, tutorials, clones, examples, docs mirrors, and case studies that are not current company signals
- unsupported social-only claims
- public company news unless it affects a startup signal
- irrelevant AI mentions

## Step 5: Enrich

For shortlisted companies, add:

- company homepage or product page
- founder/team public profile if relevant
- funding or launch source
- customer/partnership source when claimed
- GitHub/Product Hunt/press evidence when relevant

If enrichment cannot verify the company, keep the item out of the ranked company briefing and move it to a watchlist section.

## Step 6: Score

Use `references/scoring_rubric.md`.

Every selected company needs:

- total score
- dimension-level scores
- rating band
- confidence grade
- score drivers
- deductions
- evidence gaps

## Step 7: Generate HTML

Use `references/output_templates.md`.

The final HTML should make the top signal visible quickly and put details inside expandable sections.

## Failure Modes

If API fetching fails:

- Preserve any raw results already fetched.
- Explain which source failed and why.
- Continue with available sources if at least one credible source remains.
- If no current source can be fetched, produce a research plan or empty-run report instead of inventing events.

If API rate limits are hit:

- Record the source and time.
- Continue with other sources.
- Suggest lowering query count or adding an authenticated token.
