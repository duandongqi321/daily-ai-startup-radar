# Usage Guide

Daily AI Startup Radar can be used as a ChatGPT Skill or as a portable workflow in Claude, Gemini, Manus, and other capable LLMs.

The safest default is to treat the repository as an instruction bundle: give the model the core instructions, your Personal Lens profile, and any available research sources. The model should produce an English HTML briefing with verified companies only.

## Quick Start

1. Download the latest release source zip from GitHub.
2. Unzip the folder.
3. Start with onboarding or copy `config/user_profile.example.yaml` to a private `config/user_profile.yaml`.
4. Ask your LLM to create an English HTML Daily AI Startup Radar using the instructions in this repo.

Prompt:

```text
Use this Daily AI Startup Radar folder to create an English HTML briefing for the last 30 days.
Use verified companies only in ranked company cards.
Put Product Hunt launches, GitHub repos, and weak signals in a separate watchlist unless they have external company evidence.
```

## ChatGPT / Codex

Use the folder as a Skill-style instruction package.

Recommended files to include:

- `SKILL.md`
- `config/user_profile.example.yaml` or your private `config/user_profile.yaml`
- `references/research_playbook.md`
- `references/scoring_rubric.md`
- `references/output_templates.md`
- `references/signal_pipeline.md` if using API outputs

Prompt:

```text
Use $daily-ai-startup-radar to create today's English HTML Daily AI Startup Radar for me.
Use my Personal Lens profile and include only externally verifiable companies in ranked sections.
```

## Claude

Claude does not need ChatGPT Skill packaging. Use the universal prompt.

1. Open `UNIVERSAL_PROMPT.md`.
2. Paste it into Claude.
3. Attach the relevant `references/` files if the context window allows.
4. Add your profile or onboarding answers.

Prompt:

```text
Use the instructions in UNIVERSAL_PROMPT.md.
Create an English HTML Daily AI Startup Radar.
Use the last 30 days, verified companies only, and separate launch/project signals that still need verification.
```

## Gemini

Use the same approach as Claude.

Recommended attachments:

- `UNIVERSAL_PROMPT.md`
- `references/scoring_rubric.md`
- `references/output_templates.md`
- `config/user_profile.example.yaml`

Prompt:

```text
Create a self-contained English HTML briefing using this workflow.
Rank only externally verifiable AI companies.
Use Product Hunt, GitHub, and news items as discovery inputs, not automatic proof.
```

## Manus

Use Manus as a research-and-output workflow.

Recommended setup:

- Add `UNIVERSAL_PROMPT.md` as the main instruction.
- Provide `references/research_playbook.md`, `references/scoring_rubric.md`, and `references/output_templates.md`.
- Ask Manus to save the output as an `.html` file.

Prompt:

```text
Run this Daily AI Startup Radar workflow.
Research the last 30 days, verify companies with source links, score them with the rubric, and save a self-contained English HTML briefing.
```

## API-Backed Local Mode

For local signal collection:

1. Copy `.env.example` to `.env`.
2. Add private API keys locally.
3. Copy `config/sources.example.yaml` to `config/sources.yaml`.
4. Enable only the sources you can use.

Commands:

```text
python3 scripts/fetch_signals.py --dry-run
python3 scripts/fetch_signals.py --allow-insecure-ssl
python3 scripts/normalize_signals.py
```

Do not commit `.env`, `config/sources.yaml`, or any private profile file.

## Verification Rule

API results are discovery input only.

- NewsAPI/GDELT items are candidate company signals.
- Product Hunt items are launch signals until enriched.
- GitHub items are project signals until tied to a real company or product page.
- Ranked company cards require external verification and source links.

See `examples/sample-briefing.html` for the expected reading experience.
