# Output Templates

Use the user's preferred language. Default to Chinese when no preference is available. Keep English company names as written, and explain technical terms briefly.

## Daily Briefing Template

```markdown
# Daily AI Startup Radar - <YYYY-MM-DD>

Research window: <last 24h/72h>, <timezone>
Regions: Silicon Valley, New York, Singapore, Hong Kong
Profile: <short Personal Lens profile>

## 30-Second Snapshot

- <Most important pattern or signal>
- <Best founder/product lesson>
- <Most relevant Personal Lens takeaway>

## Today's Radar Picks

| Rank | Company | Region | Signal | Sector | Score | Confidence | Why it matters |
|---:|---|---|---|---|---:|---|---|
| 1 | <Company> | <Region> | <Signal> | <Sector> | <0-100> | <High/Medium/Low> | <Short reason> |

## Company Deep Dives

### 1. <Company> - <Region> - <Score>/100

**Recent signal:** <What changed recently, with date if available.>

**Beginner explanation:** <Plain-language explanation of what the company does and why customers might care.>

**Company type:** <AI agent / vertical AI / infrastructure / healthcare / finance / developer tool / etc.>

**Business and customer:** <Who pays, who uses it, and what workflow it fits into.>

**Founder/team signal:** <Publicly sourced team notes; say unknown if not available.>

**Strengths:** <2-3 concrete strengths.>

**Potential:** <Market or product upside.>

**Risks:** <2-3 concrete risks or unanswered questions.>

**Personal Lens:** <Why this matters for this user's goals. Include localization, niche version, learning, or next action when useful.>

**Sources:** <Source links.>

## Cross-Market Patterns

- <Pattern across geographies, sectors, buyer types, or business models.>

## Personal Lens Takeaways

- <What the user should learn, test, copy, avoid, or research next.>

## Watchlist

- <Company or theme to monitor next.>

## Confidence Notes

- <Source gaps, regions with weak coverage, or assumptions.>
```

## Compact Push Template

Use this when the user asks for Lark, WhatsApp, SMS, or short mobile notification formatting.

```markdown
Daily AI Startup Radar - <YYYY-MM-DD>

Top signals:
1. <Company> (<Region>) - <one-line signal>. Lens: <why user should care>.
2. <Company> (<Region>) - <one-line signal>. Lens: <why user should care>.
3. <Company> (<Region>) - <one-line signal>. Lens: <why user should care>.

Pattern: <one cross-market pattern>
Action: <one practical next action>
```

## Onboarding Result Template

After onboarding, show the user this compact profile before the first run:

```markdown
## Your Daily AI Startup Radar Profile

- Role/lens: <summary>
- Main goals: <goals>
- Regions: <regions and weights>
- Sectors: <watch sectors>
- Opportunity style: <preferences>
- Avoid: <avoid list>
- Output: <language, timezone, depth, delivery style>

I will use this as your Personal Lens for future briefings unless you change it.
```

## Company Explanation Style

Use this plain-language pattern:

```text
<Company> helps <customer> do <job> using AI. Instead of <old way>, it <new way>. This matters because <business reason>.
```

Avoid buzzword-only explanations such as:

```text
The company leverages generative AI to transform enterprise workflows.
```
