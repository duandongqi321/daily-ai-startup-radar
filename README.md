# Daily AI Startup Radar

Daily AI Startup Radar is an open-source, LLM-portable workflow for generating personalized AI startup intelligence briefings as low-friction HTML reports.

It tracks AI startup signals from the last 30 days across Silicon Valley, New York, Singapore, and Hong Kong, then explains verified companies in beginner-friendly English through a configurable Personal Lens and quantified scorecard. It is API-ready, so users can connect sources such as GitHub, GDELT, Product Hunt, NewsAPI, and Crunchbase to reduce missed current events.

## What It Does

- Finds AI startup signals from the last 30 days in target regions
- Requires ranked companies to be externally verifiable before inclusion
- Supports API-backed signal collection with safe local key handling
- Explains what each verified company does in plain English
- Analyzes company type, business model, customer, team signal, strengths, potential, and risks
- Scores companies with a quantified rubric and dimension-level evidence
- Adds a configurable Personal Lens for founder, operator, investor, career, or market-entry use cases
- Produces a self-contained HTML briefing that can be read quickly or adapted for Lark, WhatsApp, SMS, and other delivery channels

## Who It Is For

- Aspiring founders looking for startup ideas
- Builders studying AI product patterns
- Operators tracking startup, funding, and market signals
- Investors or analysts looking for early AI company signals
- People exploring how global AI startup models could be localized to APAC markets
- Anyone who wants to improve their judgment about early-stage AI companies

## How To Use

1. Download this repository or the latest release source zip.
2. Read [docs/USAGE.md](docs/USAGE.md) for ChatGPT, Claude, Gemini, Manus, and local API-backed usage.
3. Start with onboarding so the model can generate your Personal Lens profile.
4. Run the HTML briefing with a prompt like:

```text
Use $daily-ai-startup-radar to create today's HTML Daily AI Startup Radar for me.
```

For non-ChatGPT tools:

```text
Use the instructions in UNIVERSAL_PROMPT.md to create an English HTML Daily AI Startup Radar using verified companies from the last 30 days.
```

You can also ask for onboarding first:

```text
Use $daily-ai-startup-radar to onboard me and create my Personal Lens profile.
```

See [examples/sample-briefing.html](examples/sample-briefing.html) for the expected HTML reading experience.

## Use In Different LLMs

- **ChatGPT / Codex:** use `SKILL.md` as the entrypoint and include the `references/` files when needed.
- **Claude:** paste `UNIVERSAL_PROMPT.md`, attach the relevant reference files, and ask for an English HTML briefing.
- **Gemini:** use `UNIVERSAL_PROMPT.md` plus `references/scoring_rubric.md` and `references/output_templates.md`.
- **Manus:** use the workflow as a research task and ask Manus to save the final output as a self-contained HTML file.

For exact prompts, see [docs/USAGE.md](docs/USAGE.md).

## Configure Your Personal Lens

Copy the example profile and edit it:

```text
config/user_profile.example.yaml -> config/user_profile.yaml
```

Do not commit `config/user_profile.yaml` if it contains private preferences, phone numbers, webhook names, or personal context. The repo ignores that file by default.

The Personal Lens controls:

- Your role and background
- Target regions
- Sectors of interest
- Opportunity style
- Ideas or risks to avoid
- Preferred language, timezone, briefing depth, and delivery style
- Verification strictness and source requirements

## Output Experience

The default briefing is a single HTML file designed for fast reading:

- Top summary for a 30-second scan
- Ranked verified-company cards
- Total score, rating band, and confidence for each company
- Dimension-level scoring breakdown
- Risk tags and key deductions
- Expandable details for deeper reading
- Source links and evidence notes

## Signal Verification Buckets

API results are discovery inputs, not proof. The local normalization script separates signals into buckets:

- `verified_company_candidate`: promising signal that still needs source enrichment before ranking.
- `product_launch_only`: Product Hunt launch or similar product signal; useful for idea discovery but not enough for company ranking.
- `project_signal_needs_verification`: GitHub/repo-only signal; keep in watchlists until tied to a real product or company.
- `needs_verification`: thin signal that needs a product page, company source, or credible article.

Only externally verified companies should appear in ranked company cards.

## Repository Structure

```text
daily-ai-startup-radar/
|-- .gitignore
|-- .env.example
|-- CHANGELOG.md
|-- CONTRIBUTING.md
|-- LICENSE
|-- SKILL.md
|-- README.md
|-- SPEC.md
|-- UNIVERSAL_PROMPT.md
|-- agents/
|   `-- openai.yaml
|-- config/
|   |-- sources.example.yaml
|   `-- user_profile.example.yaml
|-- docs/
|   |-- PUBLISHING.md
|   `-- USAGE.md
|-- examples/
|   `-- sample-briefing.html
|-- scripts/
|   |-- fetch_signals.py
|   `-- normalize_signals.py
`-- references/
    |-- api_sources.md
    |-- onboarding.md
    |-- research_playbook.md
    |-- scoring_rubric.md
    |-- signal_pipeline.md
    |-- output_templates.md
    `-- delivery_channels.md
```
