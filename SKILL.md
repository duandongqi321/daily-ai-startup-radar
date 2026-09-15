---
name: daily-ai-startup-radar
description: Create a low-friction HTML AI startup intelligence briefing with current research, quantified scoring, and a configurable Personal Lens.
metadata:
  short-description: HTML AI startup intelligence radar
---

# Daily AI Startup Radar

Use this skill when the user asks for an AI startup radar, daily startup briefing, recent AI startup signals, or a personalized analysis of AI companies through a founder, operator, investor, career, or market-entry lens.

This skill produces research-backed intelligence, not investment, legal, tax, or hiring advice. Distinguish reported facts from your own analysis, cite sources, and state uncertainty when evidence is thin.

## Core Workflow

1. Establish the run context: briefing date, timezone, output language, recency window, target regions, and the user's profile. If `config/user_profile.yaml` exists, use it as the user's local Personal Lens unless the user provides a different profile. Default to Chinese output and the four target regions of Silicon Valley, New York, Singapore, and Hong Kong unless the user requests otherwise.
2. If no usable profile is available, read [references/onboarding.md](references/onboarding.md) and run the compact onboarding. If the user wants to skip setup, use the V0 default profile in [config/user_profile.example.yaml](config/user_profile.example.yaml) and label it as a default.
3. For a real daily briefing, browse or otherwise verify current sources. Read [references/research_playbook.md](references/research_playbook.md) before collecting signals.
4. Build a candidate list of recent AI-related startup signals, dedupe names, and prefer startups where AI is core to the product or workflow.
5. Read [references/scoring_rubric.md](references/scoring_rubric.md), score candidates with the quantified dimension standards, and select the most useful set for the user. A normal daily briefing should cover 5-7 companies, with geography balanced when evidence allows.
6. Read [references/output_templates.md](references/output_templates.md) and produce a self-contained HTML briefing by default. Use the user's preferred language for visible text and include source links for each company.
7. If the user asks to schedule, send, or push the briefing to ChatGPT, Lark, WhatsApp, SMS, or another channel, read [references/delivery_channels.md](references/delivery_channels.md). Do not claim delivery is configured unless the required scheduler, connector, webhook, or API credential is actually available and authorized.

## Default Output Contract

The default final deliverable is a single, self-contained HTML briefing optimized for minimum reading effort.

- If file creation is available, save the briefing as `daily-ai-startup-radar-YYYY-MM-DD.html` and give the user the file link plus a short summary.
- If file creation is not available, return valid HTML in a fenced `html` block.
- Use inline CSS only. Do not rely on external scripts, fonts, images, or stylesheets.
- Make the first screen useful: date, research window, top pattern, top 3 companies, score summary, and Personal Lens takeaway should be visible before deep reading.
- Use cards, chips, score bars, risk tags, source links, and `<details>` sections so users can scan first and expand only what they need.
- Every company must include total score, rating band, confidence, dimension-level score breakdown, top scoring drivers, main deductions, and source confidence notes.

## Research Defaults

- Recency window: last 24 hours for ordinary weekdays; expand to 72 hours when signals are sparse, after weekends, or when the user asks for a catch-up.
- Target geographies: Silicon Valley/San Francisco Bay Area, New York/NYC metro, Singapore, and Hong Kong.
- Startup stage: pre-seed through Series C by default. Include later-stage private AI companies only when the signal is unusually relevant.
- Signal types: funding, product launch, public beta, customer win, strategic partnership, hiring spike, accelerator/demo-day appearance, regulatory approval, open-source traction, founder announcement, acquisition rumor only if well sourced.
- Selection bias: favor companies that teach the user something about product shape, customer pain, distribution, business model, or localization opportunity.

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
