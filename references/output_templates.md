# Output Templates

Use the user's preferred language for visible copy. Default to the language in `config/user_profile.yaml` when available. Keep company names in their original language and explain technical terms briefly.

## Default Output: Self-Contained HTML

The default output is a single HTML file designed for low-effort reading. If the runtime can create files, save it as:

```text
daily-ai-startup-radar-YYYY-MM-DD.html
```

If file creation is unavailable, return the HTML in a fenced `html` block.

## Low-Effort Reading Rules

Structure the HTML so the reader can get value in three passes:

- 10 seconds: headline, date, top theme, top 3 companies, and the most relevant Personal Lens takeaway.
- 30 seconds: ranked cards with scores, confidence, signal, sector, region, and why it matters.
- 3 minutes: expandable deep dives, score breakdowns, risks, sources, and next actions.

Use:

- summary tiles
- ranked company cards
- score bars
- confidence chips
- risk tags
- short paragraphs
- source links
- `<details>` and `<summary>` for optional depth

Avoid:

- long walls of text
- large unstructured tables
- vague score numbers without explanation
- unsupported claims
- external CSS, JavaScript, images, fonts, or tracking

## Required HTML Sections

The HTML briefing must include:

1. Header: title, date, research window, regions, and profile name.
2. At-a-glance summary: top pattern, best opportunity, strongest risk, and Personal Lens takeaway.
3. Top picks: 3-6 ranked company cards.
4. Score legend: rating bands and scoring dimensions.
5. Company deep dives: one card per company with summary and expandable details.
6. Cross-market patterns.
7. Personal Lens takeaways.
8. Watchlist and next questions.
9. Sources and confidence notes.

## Company Card Requirements

Each company card must show:

- Rank
- Company name
- Region
- Sector
- Recent signal
- Beginner explanation
- Total score out of 100
- Rating band
- Confidence grade
- Risk tags
- Top scoring drivers
- Main deductions
- Dimension-level scores
- Personal Lens insight
- Source links

## HTML Skeleton

Use this skeleton as the default structure. Adapt labels to the user's language.

```html
<!doctype html>
<html lang="<language-code>">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Daily AI Startup Radar - <YYYY-MM-DD></title>
  <style>
    :root {
      --bg: #f7f8fa;
      --surface: #ffffff;
      --ink: #172026;
      --muted: #5f6b76;
      --line: #dde3ea;
      --accent: #0f766e;
      --accent-soft: #dff7f3;
      --warn: #b45309;
      --warn-soft: #fff4df;
      --risk: #b42318;
      --risk-soft: #ffebe8;
      --good: #137333;
      --good-soft: #e6f4ea;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      background: var(--bg);
      color: var(--ink);
      font: 15px/1.55 -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }
    main {
      max-width: 1120px;
      margin: 0 auto;
      padding: 28px 18px 56px;
    }
    header {
      padding: 26px;
      background: var(--surface);
      border: 1px solid var(--line);
      border-radius: 8px;
    }
    h1, h2, h3 { margin: 0; line-height: 1.18; }
    h1 { font-size: clamp(28px, 4vw, 44px); }
    h2 { font-size: 22px; margin-top: 28px; margin-bottom: 12px; }
    h3 { font-size: 18px; }
    p { margin: 8px 0 0; }
    a { color: var(--accent); }
    .meta, .muted { color: var(--muted); }
    .grid {
      display: grid;
      gap: 12px;
    }
    .summary-grid {
      grid-template-columns: repeat(4, minmax(0, 1fr));
      margin-top: 16px;
    }
    .cards {
      grid-template-columns: repeat(3, minmax(0, 1fr));
    }
    .tile, .card {
      background: var(--surface);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 16px;
    }
    .tile strong {
      display: block;
      font-size: 13px;
      color: var(--muted);
      margin-bottom: 6px;
    }
    .card-head {
      display: flex;
      gap: 12px;
      align-items: flex-start;
      justify-content: space-between;
    }
    .rank {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      min-width: 30px;
      height: 30px;
      border-radius: 999px;
      background: var(--accent-soft);
      color: var(--accent);
      font-weight: 700;
    }
    .score {
      min-width: 70px;
      text-align: right;
      font-size: 24px;
      font-weight: 800;
      color: var(--accent);
    }
    .chips {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      margin-top: 10px;
    }
    .chip {
      display: inline-flex;
      align-items: center;
      border-radius: 999px;
      padding: 4px 9px;
      background: #eef2f6;
      color: #38434f;
      font-size: 12px;
      font-weight: 600;
    }
    .chip.good { background: var(--good-soft); color: var(--good); }
    .chip.warn { background: var(--warn-soft); color: var(--warn); }
    .chip.risk { background: var(--risk-soft); color: var(--risk); }
    .score-row {
      display: grid;
      grid-template-columns: minmax(130px, 1fr) 52px minmax(120px, 2fr);
      gap: 10px;
      align-items: center;
      margin-top: 8px;
      font-size: 13px;
    }
    .bar {
      height: 8px;
      overflow: hidden;
      border-radius: 999px;
      background: #e8edf2;
    }
    .bar span {
      display: block;
      height: 100%;
      border-radius: inherit;
      background: var(--accent);
      width: var(--pct);
    }
    details {
      margin-top: 12px;
      border-top: 1px solid var(--line);
      padding-top: 12px;
    }
    summary {
      cursor: pointer;
      font-weight: 700;
    }
    ul {
      padding-left: 20px;
      margin: 8px 0 0;
    }
    .section-card {
      background: var(--surface);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 18px;
      margin-top: 12px;
    }
    @media (max-width: 860px) {
      .summary-grid, .cards { grid-template-columns: 1fr; }
      .score-row { grid-template-columns: 1fr 48px; }
      .score-row .bar { grid-column: 1 / -1; }
      header { padding: 20px; }
    }
  </style>
</head>
<body>
  <main>
    <header>
      <p class="meta"><YYYY-MM-DD> · <research-window> · <timezone></p>
      <h1>Daily AI Startup Radar</h1>
      <p class="muted">Regions: <regions> · Profile: <profile-name></p>
      <div class="grid summary-grid">
        <div class="tile"><strong>Top Theme</strong><span><top-theme></span></div>
        <div class="tile"><strong>Best Opportunity</strong><span><best-opportunity></span></div>
        <div class="tile"><strong>Main Risk</strong><span><main-risk></span></div>
        <div class="tile"><strong>Personal Lens</strong><span><personal-lens-summary></span></div>
      </div>
    </header>

    <section>
      <h2>Top Picks</h2>
      <div class="grid cards">
        <article class="card">
          <div class="card-head">
            <div>
              <span class="rank">1</span>
              <h3><company-name></h3>
              <p class="meta"><region> · <sector> · <rating-band></p>
            </div>
            <div class="score"><score>/100</div>
          </div>
          <div class="chips">
            <span class="chip good"><confidence></span>
            <span class="chip warn"><risk-tag></span>
            <span class="chip"><signal-type></span>
          </div>
          <p><strong>Signal:</strong> <recent-signal></p>
          <p><strong>Why it matters:</strong> <why-it-matters></p>
        </article>
      </div>
    </section>

    <section>
      <h2>Score Legend</h2>
      <div class="section-card">
        <p><strong>85-100:</strong> Radar Pick · <strong>70-84:</strong> Strong Watch · <strong>55-69:</strong> Useful Mention · <strong>40-54:</strong> Low-Confidence Watch</p>
        <p class="muted">Score dimensions: signal freshness, AI centrality, customer pain, business model, founder/team fit, traction, defensibility, market timing, and Personal Lens fit.</p>
      </div>
    </section>

    <section>
      <h2>Company Deep Dives</h2>
      <article class="card">
        <div class="card-head">
          <div>
            <span class="rank">1</span>
            <h3><company-name></h3>
            <p class="meta"><region> · <sector> · <company-type></p>
          </div>
          <div class="score"><score>/100</div>
        </div>
        <p><strong>Beginner explanation:</strong> <plain-language-explanation></p>
        <p><strong>Personal Lens:</strong> <user-specific-insight></p>
        <div class="chips">
          <span class="chip good"><rating-band></span>
          <span class="chip"><confidence></span>
          <span class="chip risk"><risk-tag></span>
        </div>

        <details open>
          <summary>Score Breakdown</summary>
          <div class="score-row"><span>Signal freshness</span><strong><points>/15</strong><div class="bar"><span style="--pct: <percent>%"></span></div></div>
          <div class="score-row"><span>AI centrality</span><strong><points>/15</strong><div class="bar"><span style="--pct: <percent>%"></span></div></div>
          <div class="score-row"><span>Customer pain</span><strong><points>/15</strong><div class="bar"><span style="--pct: <percent>%"></span></div></div>
          <div class="score-row"><span>Business model</span><strong><points>/10</strong><div class="bar"><span style="--pct: <percent>%"></span></div></div>
          <div class="score-row"><span>Founder/team fit</span><strong><points>/10</strong><div class="bar"><span style="--pct: <percent>%"></span></div></div>
          <div class="score-row"><span>Traction/distribution</span><strong><points>/10</strong><div class="bar"><span style="--pct: <percent>%"></span></div></div>
          <div class="score-row"><span>Defensibility</span><strong><points>/10</strong><div class="bar"><span style="--pct: <percent>%"></span></div></div>
          <div class="score-row"><span>Market timing</span><strong><points>/10</strong><div class="bar"><span style="--pct: <percent>%"></span></div></div>
          <div class="score-row"><span>Personal Lens fit</span><strong><points>/5</strong><div class="bar"><span style="--pct: <percent>%"></span></div></div>
        </details>

        <details>
          <summary>Drivers, Deductions, And Evidence</summary>
          <p><strong>Top drivers:</strong> <top-score-drivers></p>
          <p><strong>Main deductions:</strong> <main-deductions></p>
          <p><strong>Evidence gaps:</strong> <evidence-gaps></p>
        </details>

        <details>
          <summary>Business, Team, Risks, And Sources</summary>
          <p><strong>Business and customer:</strong> <business-and-customer></p>
          <p><strong>Founder/team signal:</strong> <founder-team-signal></p>
          <p><strong>Strengths:</strong> <strengths></p>
          <p><strong>Potential:</strong> <potential></p>
          <p><strong>Risks:</strong> <risks></p>
          <p><strong>Sources:</strong> <source-links></p>
        </details>
      </article>
    </section>

    <section>
      <h2>Cross-Market Patterns</h2>
      <div class="section-card"><ul><li><pattern></li></ul></div>
    </section>

    <section>
      <h2>Personal Lens Takeaways</h2>
      <div class="section-card"><ul><li><takeaway></li></ul></div>
    </section>

    <section>
      <h2>Watchlist And Next Questions</h2>
      <div class="section-card"><ul><li><watchlist-item></li></ul></div>
    </section>

    <section>
      <h2>Confidence Notes</h2>
      <div class="section-card"><p><confidence-notes></p></div>
    </section>
  </main>
</body>
</html>
```

## Compact Push Template

Use this when the user asks for Lark, WhatsApp, SMS, or short mobile notification formatting. This is not the default full output.

```markdown
Daily AI Startup Radar - <YYYY-MM-DD>

Top signals:
1. <Company> (<Region>) - <score>/100 - <one-line signal>. Lens: <why user should care>.
2. <Company> (<Region>) - <score>/100 - <one-line signal>. Lens: <why user should care>.
3. <Company> (<Region>) - <score>/100 - <one-line signal>. Lens: <why user should care>.

Pattern: <one cross-market pattern>
Action: <one practical next action>
Full HTML briefing: <link if available>
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
- Output: HTML briefing, <language>, <timezone>, <depth>

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
