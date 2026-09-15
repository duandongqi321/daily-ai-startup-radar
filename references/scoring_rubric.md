# Scoring Rubric

Score each company out of 100 using the dimensions below. The score should help the reader understand relative priority; it is not an investment recommendation.

Every company must include:

- total score
- rating band
- confidence grade
- dimension-level score breakdown
- top scoring drivers
- main deductions
- evidence gaps or source limitations

## Score Dimensions

| Dimension | Max | What It Measures |
|---|---:|---|
| Signal freshness and credibility | 15 | How recent, material, and well-sourced the startup signal is |
| AI centrality | 15 | Whether AI is core to the product, workflow, infrastructure, or data advantage |
| Customer pain and use case clarity | 15 | Whether the buyer/user and problem are specific, painful, and understandable |
| Business model and monetization | 10 | Whether there is a plausible path to revenue or strategic value |
| Founder/team fit | 10 | Whether public evidence suggests the team fits the problem |
| Traction or distribution signal | 10 | Whether there is evidence of users, customers, pilots, revenue, launch momentum, or ecosystem pull |
| Defensibility and differentiation | 10 | Whether the company has a plausible edge beyond generic AI usage |
| Market timing and potential | 10 | Whether the market is ready, growing, and important enough |
| Personal Lens fit | 5 | Whether the company is directly useful to the user's goals, target markets, and opportunity style |

## Quantitative Anchors

Use these anchors to assign each dimension score. Intermediate scores are allowed, but they must be explainable.

### 1. Signal Freshness And Credibility - 15 Points

- 0: No sourceable recent signal.
- 3: Social-only, vague, or older than 30 days.
- 6: One source, but the signal is minor, recycled, or older than 7 days.
- 10: Credible source within 7 days; signal is relevant but not highly material.
- 15: Primary or highly credible source within 72 hours; signal is material, such as funding, launch, customer win, partnership, regulatory approval, or meaningful traction.

Evidence required: source date, signal type, source link, and what changed.

### 2. AI Centrality - 15 Points

- 0: AI is not meaningfully part of the product.
- 4: AI is mostly marketing language or a small feature.
- 8: AI improves a workflow but the product could mostly exist without it.
- 12: AI is central to the user workflow, automation, decision support, or product promise.
- 15: AI is the core engine, agent, data advantage, infrastructure layer, or defensible workflow system.

Evidence required: product description, AI capability, and why AI matters to the outcome.

### 3. Customer Pain And Use Case Clarity - 15 Points

- 0: User, buyer, or problem is unclear.
- 4: Broad persona is named, but the workflow and pain are fuzzy.
- 8: Clear user and use case, but urgency or willingness to pay is uncertain.
- 12: Specific painful workflow with a clear old way and better new way.
- 15: Urgent, repeated, costly, or high-stakes pain with a clear buyer/user and strong reason to switch.

Evidence required: target customer, job to be done, old workflow, and why the pain matters.

### 4. Business Model And Monetization - 10 Points

- 0: No visible business model.
- 2: Monetization is speculative or unclear.
- 5: Plausible pricing model, but no proof of willingness to pay.
- 8: Evidence of paying customers, pilots, usage-based demand, enterprise interest, or clear budget owner.
- 10: Repeatable monetization path with strong fit between product value, buyer budget, and pricing model.

Evidence required: pricing, customer type, buyer budget, revenue signal, or monetization hypothesis.

### 5. Founder/Team Fit - 10 Points

- 0: No public team information found.
- 2: Team exists publicly, but fit to the problem is unclear.
- 5: Relevant technical, product, or domain background.
- 8: Strong founder-market fit, such as prior startup, deep industry expertise, research strength, or operator experience.
- 10: Exceptional founder-market fit plus credible execution signal, such as prior exits, notable technical work, strong customer network, or unusually relevant domain authority.

Evidence required: public founder/team source and why the background matters.

### 6. Traction Or Distribution Signal - 10 Points

- 0: No traction or distribution evidence.
- 2: Waitlist, social attention, or early announcement only.
- 5: Public launch, beta, accelerator signal, open-source activity, or credible early pilots.
- 8: Named customers, integrations, partnerships, usage metrics, revenue hints, or strong developer/community adoption.
- 10: Multiple strong traction signals or a clear distribution advantage.

Evidence required: customer, usage, launch, partnership, community, revenue, or distribution source.

### 7. Defensibility And Differentiation - 10 Points

- 0: Generic AI wrapper or no visible differentiation.
- 2: Better UX or packaging, but easy to copy.
- 5: Some workflow, data, domain, integration, or distribution edge.
- 8: Strong differentiated wedge, such as proprietary data, deep workflow lock-in, regulatory/domain expertise, hard integrations, or powerful distribution.
- 10: Compounding advantage that could strengthen over time.

Evidence required: differentiation claim and the reason it may endure.

### 8. Market Timing And Potential - 10 Points

- 0: Market is too unclear, too early, too late, or too small.
- 2: Interesting trend but unclear buyer budget or adoption timing.
- 5: Growing demand with some proof that customers are experimenting.
- 8: Clear tailwind from platform shifts, regulation, cost pressure, labor shortage, or new AI capabilities.
- 10: Large and urgent market with strong timing and visible budget movement.

Evidence required: market driver, adoption driver, or budget/timing signal.

### 9. Personal Lens Fit - 5 Points

- 0: Not relevant to the user's stated goals, markets, or opportunity style.
- 1: Interesting but distant from the user's likely actions.
- 3: Useful for learning, market mapping, or possible localization.
- 5: Directly actionable for the user's target market, sector interests, founder exploration, career path, or next experiment.

Evidence required: explicit link to the user's profile and one practical learning or action.

## Score Caps

Apply caps after adding the raw dimension scores:

- If there is no sourceable current signal, max score is 54.
- If AI centrality is unclear, max score is 69.
- If the company is not clearly a startup, max score is 59 unless it is included only as market context.
- If the briefing relies on a single weak source, max confidence is Low and max score is 69.
- If a company has strong hype but unclear buyer and no traction, max score is 64.

## Rating Bands

- 85-100: Radar Pick. Strong signal, strong evidence, and high learning value.
- 70-84: Strong Watch. Worth tracking closely.
- 55-69: Useful Mention. Interesting but incomplete, early, or less personally relevant.
- 40-54: Low-Confidence Watch. Needs more evidence.
- Below 40: Usually skip unless the user specifically asked about it.

## Confidence Grade

Confidence is separate from the score.

- High: multiple credible sources, clear recent signal, low ambiguity.
- Medium: at least one credible source, but some missing context.
- Low: early, thin, social-only, stealthy, geographically ambiguous, or materially incomplete.

## Required Scorecard Format

For each included company, create a compact scorecard in this shape before turning it into HTML:

```yaml
company: "<Company>"
total_score: 78
rating_band: "Strong Watch"
confidence: "Medium"
dimension_scores:
  signal_freshness_and_credibility: "12/15"
  ai_centrality: "13/15"
  customer_pain_and_use_case_clarity: "11/15"
  business_model_and_monetization: "7/10"
  founder_team_fit: "7/10"
  traction_or_distribution_signal: "6/10"
  defensibility_and_differentiation: "7/10"
  market_timing_and_potential: "9/10"
  personal_lens_fit: "4/5"
top_scoring_drivers:
  - "<driver>"
main_deductions:
  - "<deduction>"
evidence_gaps:
  - "<gap>"
```

Check the arithmetic. Personal Lens fit must not exceed 5 points.

## Risk Tags

Use risk tags to keep analysis honest:

- "unclear buyer"
- "crowded category"
- "weak differentiation"
- "regulatory risk"
- "platform dependency"
- "capital intensive"
- "data access risk"
- "long enterprise sales cycle"
- "unclear AI depth"
- "source confidence low"

## Scoring Notes

- Do not let funding amount dominate the score.
- A small company with a sharp workflow and strong Personal Lens can outrank a heavily funded but generic company.
- If the company is exciting but evidence is thin, give a promising score with lower confidence rather than inflating certainty.
- If the company is not clearly a startup, reduce score unless the signal directly affects startup opportunity discovery.
- If a claim cannot be sourced, omit it or mark it as uncertain; do not use unsupported claims to increase the score.
