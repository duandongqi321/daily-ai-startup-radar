---
name: daily-ai-startup-radar
description: Create an English, low-friction HTML AI startup intelligence briefing using only verifiable real companies, API-ready research, quantified scoring, and a configurable Personal Lens.
metadata:
  short-description: Verified AI startup HTML radar
---

# Daily AI Startup Radar

Use this skill when the user asks for an AI startup radar, startup intelligence briefing, recent AI startup signals, or a personalized analysis of verified AI companies through a founder, operator, investor, career, or market-entry lens.

This skill produces research-backed intelligence, not investment, legal, tax, or hiring advice. Distinguish reported facts from your own analysis, cite sources, and state uncertainty when evidence is thin.

## Core Workflow

1. Establish the run context: briefing date, timezone, output language, recency window, target regions, and the user's profile. If `config/user_profile.yaml` exists, use it as the user's local Personal Lens unless the user provides a different profile. Default to English output, a 30-day research window, and the four target regions of Silicon Valley, New York, Singapore, and Hong Kong unless the user requests otherwise.
2. If no usable profile is available, read [references/onboarding.md](references/onboarding.md) and run the compact onboarding. If the user wants to skip setup, use the V0 default profile in [config/user_profile.example.yaml](config/user_profile.example.yaml) and label it as a default.
3. For a real briefing, browse or otherwise verify current sources. Read [references/research_playbook.md](references/research_playbook.md) before collecting signals. If the user wants API-backed collection or `config/sources.yaml` exists, also read [references/api_sources.md](references/api_sources.md) and [references/signal_pipeline.md](references/signal_pipeline.md).
4. Build a candidate list of recent AI-related startup signals, dedupe names, and prefer startups where AI is core to the product or workflow. When local execution is available and API sources are configured, use `scripts/fetch_signals.py` and `scripts/normalize_signals.py` to collect and normalize raw signals before analysis.
5. Apply the verified-company gate before scoring. A company may appear in Top Picks or Company Deep Dives only when it is a real, externally verifiable company with enough evidence to cite. GitHub-only repositories, demos, templates, student projects, or personal experiments can appear only in a separate watchlist or "needs verification" section.
6. Read [references/scoring_rubric.md](references/scoring_rubric.md), score verified companies with the quantified dimension standards, and select the most useful set for the user. A normal briefing should cover 5-7 verified companies when enough evidence exists; otherwise include fewer and clearly explain the gap.
7. Read [references/output_templates.md](references/output_templates.md) and produce a self-contained English HTML briefing by default. Include source links for each company.
8. If the user asks to schedule, send, or push the briefing to ChatGPT, Lark, WhatsApp, SMS, or another channel, read [references/delivery_channels.md](references/delivery_channels.md). Do not claim delivery is configured unless the required scheduler, connector, webhook, or API credential is actually available and authorized.

## Default Output Contract

The default final deliverable is a single, self-contained HTML briefing optimized for minimum reading effort.

- If file creation is available, save the briefing as `daily-ai-startup-radar-YYYY-MM-DD.html` and give the user the file link plus a short summary.
- If file creation is not available, return valid HTML in a fenced `html` block.
- Use inline CSS only. Do not rely on external scripts, fonts, images, or stylesheets.
- Make the first screen useful: date, research window, top pattern, top 3 companies, score summary, and Personal Lens takeaway should be visible before deep reading.
- Use cards, chips, score bars, risk tags, source links, and `<details>` sections so users can scan first and expand only what they need.
- Every company must include total score, rating band, confidence, dimension-level score breakdown, top scoring drivers, main deductions, and source confidence notes.
- Visible briefing text must be in English by default, even when onboarding answers or user notes are in another language, unless the user explicitly requests a different output language.

## Research Defaults

- Recency window: last 30 days by default. Daily runs should refresh the same 30-day window and highlight what is newly discovered or materially updated, rather than forcing a 24-hour news window.
- Target geographies: Silicon Valley/San Francisco Bay Area, New York/NYC metro, Singapore, and Hong Kong.
- Startup stage: pre-seed through Series C by default. Include later-stage private AI companies only when the signal is unusually relevant.
- Signal types: funding, product launch, public beta, customer win, strategic partnership, hiring spike, accelerator/demo-day appearance, regulatory approval, open-source traction, founder announcement, acquisition rumor only if well sourced.
- Selection bias: favor companies that teach the user something about product shape, customer pain, distribution, business model, or localization opportunity.

## Verified Company Gate

Do not present a candidate as a company unless it is externally verifiable.

Minimum inclusion requirement for Top Picks and Company Deep Dives:

- A company homepage, product page, official blog, credible news item, investor/accelerator page, Product Hunt launch, Crunchbase/company database profile, LinkedIn company page, or public founder/team source.
- At least two useful source links when possible. One source may be acceptable only if it is a strong primary source and the briefing clearly marks any missing context.
- A clear distinction between the company, its product, and any GitHub repository or technical demo.

GitHub-only evidence is discovery input, not company verification. If a promising repository cannot be tied to a real company or product page, label it as "Project signal - needs verification" and keep it out of the company ranking.

## API-Ready Research Mode

The skill can use API-backed signal collection when the user provides credentials or a local `.env` file.

- Public templates: `.env.example` and `config/sources.example.yaml`.
- Private local files: `.env` and `config/sources.yaml`. These must not be committed.
- Raw API output should be treated as discovery input, not truth. Every included claim still needs source review, deduplication, confidence grading, and scoring.
- Missing API keys are not blockers. Skip unavailable sources and continue with available sources or manual web research.
- When only GitHub is available, produce a discovery/watchlist report or use web research to verify companies before creating a company briefing.

## Personal Lens

The Personal Lens converts startup news into user-specific insight. Use the profile fields for background, goals, markets, sector interests, constraints, risk appetite, and preferred learning outcomes.

For each company, answer:

- Why might this matter to this specific user?
- What can the user learn, copy, localize, avoid, or track?
- Does the company suggest a niche, APAC localization, vertical AI, distribution, partnership, or career opportunity?
- What would be a practical next question or next action?

When the profile is incomplete, make conservative assumptions and say what you assumed.

## Quality Bar

- Explain each company as if the reader is smart but new to the sector. Avoid unexplained jargon.
- Include company type, business model, customer, founder/team signal, strengths, market potential, risks, Personal Lens, score, confidence, and scoring rationale.
- Never invent funding amounts, valuations, investors, customer names, founder credentials, locations, or launch dates.
- Do not over-index on hype. A useful "why this may fail" section is part of the product.
- Prefer fewer well-supported companies over many shallow mentions.
- Keep daily outputs scannable. Put the highest-signal takeaways before long company notes, and make the HTML readable on mobile.
