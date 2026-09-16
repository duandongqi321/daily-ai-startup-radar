# Changelog

## 0.4.0 - 2026-09-16

- Improved GitHub signal queries for AI agents, vertical AI, healthcare AI, career AI, and sports AI.
- Added local candidate quality scoring before full briefing analysis.
- Filtered common false positives such as starter kits, templates, tutorials, clones, hackathons, workshops, docs mirrors, and awesome lists.
- Fixed GitHub deduplication so separate repositories are no longer collapsed into one `github.com` candidate.
- Added candidate quality reasons, deductions, source confidence, and provider metadata to normalized signal output.

## 0.3.0 - 2026-09-16

- Added API-ready source configuration with `config/sources.example.yaml`.
- Added `.env.example` for safe local API key handling.
- Added API source guidance and signal pipeline references.
- Added local helper scripts for fetching raw signals and normalizing candidates.
- Updated the core workflow to support API-backed research while keeping manual source verification.

## 0.2.0 - 2026-09-15

- Made self-contained HTML the default briefing format.
- Added low-friction reading requirements for summary, cards, score bars, risk tags, and expandable details.
- Expanded company scoring into quantified dimension-level standards.
- Required every company to include score drivers, deductions, confidence, and evidence notes.

## 0.1.0 - 2026-09-15

- Initial open-source V0.
- Added core `SKILL.md` instructions.
- Added onboarding, research, scoring, output, and delivery references.
- Added configurable Personal Lens example profile.
- Added GitHub-ready README, MIT License, gitignore, and contribution guide.
