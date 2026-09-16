# Daily AI Startup Radar V0.3 Spec

## One-Line Goal

Help a user turn daily AI startup noise into a low-friction, evidence-backed, personally relevant HTML startup radar.

## User Job

The user wants to know which recent AI startup signals are worth attention, what each company actually does, why it might matter, and what can be learned or adapted for the user's own founder, career, investment, or market-entry goals.

## V0 Scope

- Track recent AI-related startup signals across Silicon Valley, New York, Singapore, and Hong Kong through web research and optional API-backed collection.
- Explain each selected company in beginner-friendly language.
- Analyze company type, business, customer, founder/team, strength, potential, risk, and Personal Lens.
- Score companies with a transparent, quantified rubric and visible dimension breakdown.
- Produce a daily HTML briefing that can be scanned quickly, opened as a standalone file, or reformatted for push channels.
- Run compact onboarding when no user profile exists.
- Provide API source configuration templates and local helper scripts for raw signal collection and normalization.

## Non-Goals

- Do not provide financial, legal, tax, or investment advice.
- Do not claim real-time monitoring or delivery unless the environment has an authorized scheduler and delivery integration.
- Do not include private personal data about founders or employees.
- Do not rank companies only by hype, funding size, or media visibility.

## Primary Inputs

- User profile and Personal Lens configuration.
- Briefing date and timezone.
- Target regions and weights.
- Sector interests.
- Recency window.
- Output language, HTML format preference, and delivery style.
- Available research tools and delivery integrations.
- Optional API source configuration and local environment credentials.

## Candidate Signals

Good startup signals include:

- Funding announcement
- Product launch or public beta
- Customer or partnership announcement
- Accelerator, demo day, or incubator appearance
- Hiring pattern suggesting new product or market expansion
- Open-source or developer traction
- Regulatory clearance or market-entry approval
- Founder/operator announcement with credible context

## API-Ready Signal Collection

The V0.3 pipeline supports:

- `.env.example` for local credential names
- `config/sources.example.yaml` for source configuration
- `references/api_sources.md` for source roles and credential handling
- `references/signal_pipeline.md` for the raw-signal to candidate workflow
- `scripts/fetch_signals.py` for raw API collection
- `scripts/normalize_signals.py` for candidate normalization and deduplication

Raw API results are discovery inputs only. They must still be verified, deduplicated, filtered, enriched, scored, and cited before appearing in a briefing.

## Output Shape

A normal daily briefing should include:

1. Self-contained HTML document with inline CSS
2. Header with date, timezone, regions, research window, and profile
3. First-screen executive snapshot for a 30-second read
4. Ranked top picks with score, rating band, confidence, and risk tags
5. Company cards with quantified score breakdowns
6. Expandable deep-dive sections for business, founder/team, strengths, potential, risks, Personal Lens, and sources
7. Cross-market patterns and Personal Lens takeaways
8. Watchlist, next questions, sources, and confidence notes

## Quantified Scoring

Every included company must show:

- Total score out of 100
- Rating band
- Confidence grade
- Dimension-level scores
- Top scoring drivers
- Main score deductions
- Evidence gaps or source limitations

The scoring dimensions are defined in `references/scoring_rubric.md`.

## Personal Lens Model

The Personal Lens should connect each startup to:

- User background
- User goals
- Target markets
- Sector interests
- Skills, network, and unfair advantages
- Constraints and avoid-list
- Preferred opportunity style

Example lens questions:

- Can this idea be localized to APAC, Hong Kong, Singapore, or another target market?
- Is there a smaller niche version a solo founder or small team could test?
- What product or go-to-market pattern is worth copying?
- What risk or blind spot should the user avoid?
- What should the user research next?

## V0 Success Criteria

- The user can upload the folder as a Skill package.
- The Skill can onboard a new user without needing a long back-and-forth.
- A daily HTML briefing can be produced from current sources with clear citations.
- The output feels useful to a beginner but still sharp enough for founder thinking.
- The Personal Lens changes the analysis, instead of being a generic final paragraph.
- The score is explainable at the dimension level, not just a single number.
- API-backed collection can run without committing credentials and can skip unavailable sources safely.

## V1 Ideas

- Add Lark webhook formatting and delivery helper.
- Add WhatsApp Business Cloud API formatting.
- Add SMS summaries through Twilio or another provider.
- Add saved watchlists by company, sector, and founder.
- Add weekly pattern review and "startup ideas generated from this week's signals."
- Add a structured database or spreadsheet export.
- Add stronger provider-specific enrichers for paid data sources.
