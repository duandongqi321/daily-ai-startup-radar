# Onboarding

Use onboarding when the user has not provided a profile or asks to configure the Personal Lens.

Keep onboarding lightweight. The goal is to collect enough context to make the daily radar personally useful, not to make the user fill out a long form.

## Compact 5-Minute Onboarding

Ask these questions in the user's language. Let the user answer in free text, bullet points, or option letters.

1. What best describes you right now? Choose any that fit: aspiring founder, current founder, investor, operator, job seeker, student/researcher, big-company employee, other.
2. In 1-3 sentences, what is your background?
3. What do you want this radar to help with? Choose up to 3: startup ideas, AI product learning, funding trends, localizing overseas ideas, job search, partnerships, investment ideas, training judgment.
4. Which regions should it track? Defaults: Silicon Valley, New York, Singapore, Hong Kong. Add or remove any regions.
5. Which AI sectors do you care about most? Choose up to 5: vertical AI, agents, infrastructure, developer tools, healthcare, finance, legal, education, consumer apps, robotics/hardware, data/evaluation, security, SMB, commerce, recruiting/career, bio/life sciences, creator/media.
6. What kind of opportunities are most interesting? Examples: quick solo-founder tests, B2B workflow tools, local services, enterprise SaaS, consumer apps, marketplaces, APIs, data products.
7. What should the radar avoid? Examples: heavy regulation, crypto, hardware, defense, enterprise-only sales, ideas needing large capital, anything outside your values.
8. What output style do you prefer? Options: concise daily digest, standard briefing, deep-dive briefing, Lark-friendly compact format, WhatsApp/SMS summary.
9. What timezone should it use? English is the default output language unless you explicitly prefer another language.

## Optional 15-Minute Deepening

Use these only when the user wants a stronger Personal Lens.

- What industries do you understand better than most people?
- What networks, geography, language ability, professional experience, or distribution advantages can you use?
- What customer groups can you reach for discovery interviews?
- What startup patterns do you want to learn from: AI agents, vertical SaaS, workflow automation, data moats, community-led growth, marketplaces, API products, services-to-software?
- What does a "good opportunity" look like for you in the next 3-6 months?
- What would make an opportunity a bad fit even if it is objectively promising?
- Are you optimizing for learning, income, venture-scale upside, career transition, or community building?

## Profile Synthesis

After onboarding, summarize the profile in this shape:

```yaml
profile_name: "<short profile name>"
language: "<preferred language>"
timezone: "<IANA timezone>"
target_regions:
  - name: "<region>"
    weight: "<high|medium|low>"
personal_lens:
  user_type: []
  background_summary: ""
  goals: []
  watch_sectors: []
  opportunity_preferences: []
  avoid: []
  risk_appetite: "<low|medium|high>"
  personal_lens_questions: []
briefing:
  recency_window_hours: 720
  fallback_recency_window_hours: 720
  max_companies: 6
  preferred_depth: "standard"
  require_verified_companies: true
delivery:
  chatgpt:
    enabled: true
```

Tell the user they can edit the profile anytime. Do not claim it has been permanently saved unless the environment provides persistent memory or a file has actually been created.

## Default V0 Profile

If the user wants to start immediately, use the example profile in `config/user_profile.example.yaml`. Label it as a default APAC-founder learning profile and invite the user to refine it later.
