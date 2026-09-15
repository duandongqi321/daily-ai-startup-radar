# Daily AI Startup Radar V0 Spec

## One-Line Goal

Help a user turn daily AI startup noise into a small, evidence-backed, personally relevant startup radar.

## User Job

The user wants to know which recent AI startup signals are worth attention, what each company actually does, why it might matter, and what can be learned or adapted for the user's own founder, career, investment, or market-entry goals.

## V0 Scope

- Track recent AI-related startup signals across Silicon Valley, New York, Singapore, and Hong Kong.
- Explain each selected company in beginner-friendly language.
- Analyze company type, business, customer, founder/team, strength, potential, risk, and Personal Lens.
- Score companies with a transparent rubric.
- Produce a daily briefing that can be read in chat or reformatted for push channels.
- Run compact onboarding when no user profile exists.

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
- Output language and format preference.
- Available research tools and delivery integrations.

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

## Output Shape

A normal daily briefing should include:

1. Header with date, timezone, regions, and research window
2. Executive snapshot
3. Top radar picks table
4. Company deep dives
5. Patterns observed across regions or sectors
6. Personal Lens takeaways
7. Watchlist and next questions
8. Sources and confidence notes

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
- A daily briefing can be produced from current sources with clear citations.
- The output feels useful to a beginner but still sharp enough for founder thinking.
- The Personal Lens changes the analysis, instead of being a generic final paragraph.

## V1 Ideas

- Add Lark webhook formatting and delivery helper.
- Add WhatsApp Business Cloud API formatting.
- Add SMS summaries through Twilio or another provider.
- Add saved watchlists by company, sector, and founder.
- Add weekly pattern review and "startup ideas generated from this week's signals."
- Add a structured database or spreadsheet export.
