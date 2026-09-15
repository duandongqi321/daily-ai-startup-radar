# Contributing

Thanks for helping improve Daily AI Startup Radar.

## Good Contributions

- Better onboarding questions
- Stronger research instructions
- Better scoring criteria
- New output templates for different user types
- Safer delivery-channel guidance
- Examples that make the Skill easier to adapt
- Localization improvements

## Contribution Principles

- Keep the Skill useful for many people, not only one user profile.
- Do not commit personal profiles, webhook URLs, phone numbers, tokens, private notes, or non-public company information.
- Separate reported facts from analysis.
- Do not frame the output as investment, legal, tax, or hiring advice.
- Prefer concise, reusable instructions over long generic explanations.

## Local Profiles

Use `config/user_profile.example.yaml` as the public template.

Create your private local profile as:

```text
config/user_profile.yaml
```

That file is ignored by git by default.

## Pull Request Checklist

- `SKILL.md` still has valid YAML frontmatter.
- New references are linked from `SKILL.md` or another relevant reference file.
- No secrets or personal profile details are included.
- The README still explains how to use the Skill.
- The change improves a repeatable workflow, not just one temporary briefing.
