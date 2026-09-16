# Daily AI Startup Radar

Daily AI Startup Radar is an open-source ChatGPT Skill for generating personalized AI startup intelligence briefings as low-friction HTML reports.

It tracks recent AI startup signals across Silicon Valley, New York, Singapore, and Hong Kong, then explains each company in beginner-friendly language through a configurable Personal Lens and quantified scorecard. It is API-ready, so users can connect sources such as GitHub, GDELT, Product Hunt, NewsAPI, and Crunchbase to reduce missed current events.

## What It Does

- Finds recent AI startup signals from target regions
- Supports API-backed signal collection with safe local key handling
- Explains what each company does in plain language
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

1. Download this repository or the release zip.
2. Upload the Skill folder or zip file to ChatGPT Skills.
3. Start with onboarding so ChatGPT can generate your Personal Lens profile.
4. Run the HTML briefing with a prompt like:

```text
Use $daily-ai-startup-radar to create today's HTML Daily AI Startup Radar for me.
```

You can also ask for onboarding first:

```text
Use $daily-ai-startup-radar to onboard me and create my Personal Lens profile.
```

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

## Output Experience

The default briefing is a single HTML file designed for fast reading:

- Top summary for a 30-second scan
- Ranked company cards
- Total score, rating band, and confidence for each company
- Dimension-level scoring breakdown
- Risk tags and key deductions
- Expandable details for deeper reading
- Source links and evidence notes

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
|-- agents/
|   `-- openai.yaml
|-- config/
|   |-- sources.example.yaml
|   `-- user_profile.example.yaml
|-- docs/
|   `-- PUBLISHING.md
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

## V0 Defaults

- Regions: Silicon Valley, New York, Singapore, and Hong Kong
- Research window: last 24 hours by default; expands to 72 hours after weekends or when signals are sparse
- Company count: 5-7 companies per standard briefing
- Output format: self-contained HTML
- Language: configurable by user profile
- Focus: startup ideas, product patterns, business models, risks, and localization opportunities

## API-Ready Mode

The repository includes source templates and helper scripts for local API-backed collection:

```text
cp .env.example .env
cp config/sources.example.yaml config/sources.yaml
python scripts/fetch_signals.py --dry-run
python scripts/fetch_signals.py
python scripts/normalize_signals.py
```

Do not commit `.env` or `config/sources.yaml`. Keep real API keys local.

API-backed collection is optional. Without keys, the Skill can still run from web research and manual source review.

## Delivery Notes

This Skill creates the research workflow and briefing. Automatic delivery to Lark, WhatsApp, SMS, or mobile notifications requires an external scheduler, webhook, API token, or connector.

See `references/delivery_channels.md` for guidance on adapting the briefing format for different delivery channels.

## Boundaries

- The Skill does not send messages automatically unless the runtime has an authorized delivery tool.
- It does not provide investment, legal, tax, or hiring advice.
- If current research tools are unavailable, it should produce a template or research plan rather than pretending to verify daily signals.
- Funding, founder, customer, and traction claims should be cited. Weak evidence should be marked clearly.

## Contributing

Contributions are welcome. Good improvements include better onboarding questions, stronger research instructions, clearer scoring, new user profile examples, and additional delivery templates.
