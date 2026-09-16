# API Sources

Use this reference when the user wants API-backed signal collection or when a scheduled run should reduce missed current events.

## Principle

APIs should improve recall, not replace judgment. Treat API results as raw signals that still need deduplication, source checks, scoring, and Personal Lens analysis.

Never commit API keys. Read keys from environment variables or a local `.env` file that is ignored by git.

## Recommended Source Stack

Start with a simple multi-source stack:

1. GitHub Search API for open-source AI infra, developer tools, and repo traction.
2. GDELT DOC API for broad news/event coverage.
3. Product Hunt API for launch signals.
4. RSS feeds from company blogs, VC blogs, accelerators, and local ecosystem sources.
5. Optional paid/company-data APIs such as Crunchbase when available.

This mix catches different signal types. No single API is enough.

## Source Roles

### GitHub

Best for:

- AI infrastructure
- developer tools
- open-source agents
- early technical traction

Important:

- GitHub is a discovery source, not company verification.
- A repository can be real while the company is not yet verifiable.
- Do not promote a GitHub-only item into Top Picks or Company Deep Dives unless it is tied to a verified company, official product page, credible launch, or public founder/company source.

Useful signals:

- recently created repositories
- recent push activity
- star growth
- forks
- project description and topics

Auth:

- Optional for low-volume use, recommended for higher rate limits.
- Environment variable: `GITHUB_TOKEN`

Official docs: https://docs.github.com/en/rest/search/search

### GDELT

Best for:

- news coverage
- regional startup events
- product launches
- partnerships
- policy or regulator-adjacent signals

Useful signals:

- article title
- article URL
- source domain
- publication date
- region keywords

Auth:

- Usually not required for the public DOC API.
- Environment variable is left blank by default.

Local note:

- On some macOS Python installations, HTTPS requests can fail with a local certificate error. Fixing local Python certificates is preferred. For one-off local testing only, `scripts/fetch_signals.py --allow-insecure-ssl` can bypass certificate verification.

Official docs: https://www.gdeltproject.org/ and https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/

### Product Hunt

Best for:

- new product launches
- consumer AI apps
- developer tools
- agent experiments
- indie and early-stage product discovery

Useful signals:

- launch date
- tagline
- topics
- votes
- website
- maker comments when available

Auth:

- Required.
- Environment variable: `PRODUCTHUNT_TOKEN`

Official docs: https://www.producthunt.com/v2/docs

### NewsAPI

Best for:

- secondary news coverage
- broad media sweep
- fallback search when GDELT is noisy

Auth:

- Required.
- Environment variable: `NEWSAPI_KEY`

Official docs: https://newsapi.org/docs

### Crunchbase

Best for:

- funding data
- investor data
- company profiles
- category enrichment

Notes:

- Access and available fields depend on plan level.
- Use Crunchbase primarily for enrichment, not as the only source of current signals.

Auth:

- Required.
- Environment variable: `CRUNCHBASE_API_KEY`

Official docs: https://data.crunchbase.com/docs

## Source Selection Rules

- Use at least two source categories when possible: one discovery source and one verification/enrichment source.
- Do not include a company only because it appeared in an API response.
- Do not include a company only because a GitHub repository exists.
- Down-rank stale results, generic AI wrappers, and weak source matches.
- Preserve source URLs and timestamps through the whole pipeline.
- Mark source confidence as Low when the only evidence is a social post, vague launch page, or thin metadata.

## Environment Variables

Use `.env.example` as the public template and `.env` for local secrets:

```text
PRODUCTHUNT_TOKEN=""
GITHUB_TOKEN=""
NEWSAPI_KEY=""
GDELT_API_KEY=""
CRUNCHBASE_API_KEY=""
```

`.env` must stay ignored by git.
