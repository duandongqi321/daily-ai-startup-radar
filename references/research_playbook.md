# Research Playbook

Use this playbook before producing a real daily briefing.

## Research Objective

Find AI-related startup signals from the last 30 days that are useful for the user's Personal Lens. Prioritize sources that prove the company is real, explain what changed recently, and show why the company is worth tracking.

## Source Hierarchy

Prefer sources in this order:

1. Primary sources: company websites, official blogs, press releases, founder posts, product pages, docs, investor announcements, accelerator pages, government or regulator pages.
2. High-quality secondary sources: reputable technology, startup, business, local ecosystem, or industry publications.
3. Market context sources: analyst notes, ecosystem reports, industry databases, public company/customer pages, GitHub/Product Hunt/Hacker News only when relevant.
4. Social posts: use only as a signal unless corroborated by a stronger source.

Do not use private, leaked, or doxxing-style information. Founder/team notes should come from public professional sources.

## Verified Company Gate

Top Picks and Company Deep Dives must contain real, externally verifiable companies only.

Include a company only when at least one of these is available:

- company homepage, product page, official blog, or press release
- credible news article, funding announcement, investor post, accelerator page, or public partnership/customer announcement
- company database or launch profile such as Crunchbase, Product Hunt, Wellfound, YC, TechCrunch profile coverage, LinkedIn company page, or equivalent
- public founder/team source tied to the product or company

Use at least two useful source links when possible. A single source is acceptable only when it is a strong primary source and the briefing clearly marks the missing context.

Do not include these in company rankings unless independently verified as a real company:

- GitHub-only repositories
- personal projects
- student/class projects
- templates, starter kits, clones, demos, awesome lists, docs mirrors, or case studies
- vague "AI startup" mentions with no company page or sourceable team/product evidence

If a signal is interesting but not company-verified, put it in a separate "Project Signals To Verify" or "Watchlist" section.

## Region Definitions

- Silicon Valley: San Francisco Bay Area, San Jose, Palo Alto, Menlo Park, Mountain View, Redwood City, Oakland, Berkeley, and nearby venture ecosystem signals.
- New York: New York City and NYC metro startup ecosystem.
- Singapore: Singapore-headquartered startups or AI companies with meaningful Singapore/APAC signal.
- Hong Kong: Hong Kong-headquartered startups or AI companies with meaningful Hong Kong/APAC signal.

If a company is remote-first or has unclear geography, assign the region based on headquarters, founder base, market signal, or funding ecosystem, and state the basis.

## Search Strategy

Run several targeted searches instead of one broad search. Search the last 30 days by default. Combine:

- Region terms: "San Francisco AI startup", "Silicon Valley AI startup", "New York AI startup", "Singapore AI startup", "Hong Kong AI startup"
- Signal terms: funding, seed, Series A, launch, beta, partnership, customer, accelerator, demo day, hiring, open source
- Sector terms from the user's profile
- Date filters when available

Useful query patterns:

```text
"AI startup" "funding" "San Francisco" <date/month>
"AI startup" "New York" "launched" OR "raises"
"Singapore" "AI startup" "seed" OR "Series A"
"Hong Kong" "AI startup" "partnership" OR "launch"
"AI agent startup" "raises" "New York"
"vertical AI" startup "Singapore"
```

## Candidate Intake Table

For each candidate, capture:

```text
company:
verification_status:
verification_sources:
region:
source_date:
signal_type:
one_sentence_signal:
ai_is_core: yes/no/unclear
stage:
sector:
customer:
business_model:
founder_team_signal:
traction_signal:
scoring_evidence:
  freshness:
  ai_centrality:
  customer_pain:
  business_model:
  founder_team_fit:
  traction_distribution:
  defensibility:
  market_timing:
  personal_lens_fit:
source_links:
notes:
```

## Evidence Rules

- Use at least one strong current source per included company; two useful sources are the default target.
- Cite every funding amount, investor, launch, partnership, customer, founder background, regulatory approval, or traction claim.
- If evidence is weak, downgrade confidence instead of filling gaps.
- If no strong current signals exist in a region, say so and include the best available watchlist item with lower confidence.
- Do not repeat stale companies just because they are famous.

## Selection Rules

Start from 10-20 candidates when possible, then choose 5-7 companies for the briefing.

Prefer candidates with:

- A recent, sourceable signal
- External evidence that the company is real and findable
- AI as a core product capability, not just marketing language
- A clear user or buyer
- A product wedge that teaches something
- Personal Lens relevance
- Enough evidence to score at the dimension level
- Regional diversity across the four target markets

Reject or down-rank:

- Generic AI wrappers with no clear workflow
- Repo-only projects with no company/product verification
- Companies with only vague stealth claims
- Old funding news outside the window
- Large public companies unless they are relevant context for a startup signal
- Unsupported social media rumors

## Analysis Discipline

Separate three layers:

- Fact: what sources directly report
- Inference: your interpretation based on available evidence
- Personal Lens: why it matters to this user

When making an inference, use language like "This suggests..." or "A reasonable hypothesis is..." rather than presenting it as fact.
