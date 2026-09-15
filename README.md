# Daily AI Startup Radar

Daily AI Startup Radar is an open-source ChatGPT Skill for generating a personalized daily AI startup intelligence briefing.

It tracks recent AI startup signals across Silicon Valley, New York, Singapore, and Hong Kong, then explains each company in beginner-friendly language with a configurable Personal Lens.

中文简介：这是一个 V0 版 ChatGPT Skill，用来每天生成个性化 AI 创业情报简报，帮助用户从 startup 新闻里找到创业灵感、产品模式、风险判断和本地化机会。

## What It Does

- Finds recent AI startup signals from target regions
- Explains what each company does in plain language
- Analyzes company type, business model, customer, team signal, strengths, potential, and risks
- Scores companies with a transparent rubric
- Adds a configurable Personal Lens for founder, investor, operator, career, or market-entry use cases
- Produces a daily briefing that can be used in ChatGPT or adapted for Lark, WhatsApp, SMS, and other delivery channels

## Who It Is For

- 正在找创业方向的人
- 想学习 AI startup 产品形态的人
- 想观察融资、产品和市场趋势的人
- 想把海外模式本地化到 APAC、香港或新加坡的人
- 想训练自己判断 early-stage startup 能力的人

## Repository Structure

```text
daily-ai-startup-radar/
|-- .gitignore
|-- CHANGELOG.md
|-- CONTRIBUTING.md
|-- LICENSE
|-- SKILL.md
|-- README.md
|-- SPEC.md
|-- agents/
|   `-- openai.yaml
|-- config/
|   `-- user_profile.example.yaml
|-- docs/
|   `-- PUBLISHING.md
`-- references/
    |-- onboarding.md
    |-- research_playbook.md
    |-- scoring_rubric.md
    |-- output_templates.md
    `-- delivery_channels.md
```

## Quick Start

1. 上传这个 Skill 文件夹，或上传生成的 `daily-ai-startup-radar.zip`。
2. 第一次运行时，让 ChatGPT 使用 onboarding 问题帮你生成个人 profile。
3. 之后每天使用类似提示：

```text
Use $daily-ai-startup-radar to create today's Daily AI Startup Radar for me.
```

中文也可以：

```text
使用 $daily-ai-startup-radar，按我的 Personal Lens 生成今天的 AI 创业雷达。
```

## Configure Your Personal Lens

Copy the example profile and edit it:

```text
config/user_profile.example.yaml -> config/user_profile.yaml
```

Do not commit `config/user_profile.yaml` if it contains private preferences, phone numbers, webhook names, or personal context. This repo ignores that file by default.

The Personal Lens controls:

- your role and background
- your target regions
- your sectors of interest
- what opportunities you want to find
- what ideas or risks to avoid
- your preferred language, timezone, briefing depth, and delivery style

## V0 Defaults

- 地区：Silicon Valley、New York、Singapore、Hong Kong
- 时间窗口：默认过去 24 小时；周末后或信号较少时扩展到 72 小时
- 公司数量：5-7 家
- 输出语言：默认中文，可按用户语言切换
- 输出重点：创业启发、产品形态、商业模式、风险、APAC/本地化机会

## Delivery Notes

这个 Skill 本身负责研究、筛选、分析和生成简报。要自动推送到 Lark、WhatsApp、短信或手机通知，还需要外部调度器、ChatGPT scheduled task、webhook、API token 或对应连接器。

V0 已经包含 `references/delivery_channels.md`，用于指导后续把日报改成适合 Lark、WhatsApp、SMS 或 ChatGPT 通知的格式。

## Current Boundaries

- 不会自动发送消息，除非运行环境已经有可用且授权的发送工具。
- 不会提供投资建议。
- 如果没有联网研究能力，应该只输出模板、流程或待研究清单，不能假装已经核验了当天信息。
- 对创始人背景、融资数据和客户案例必须引用来源；来源不足时要标注不确定。

## Publish This Skill

See [docs/PUBLISHING.md](docs/PUBLISHING.md) for step-by-step GitHub publishing instructions.

## ChatGPT Skill Convention

OpenAI Skills use `SKILL.md` as the core instruction file, with optional supporting files in the same Skill folder. This project follows that pattern: the entrypoint stays short, and detailed onboarding, research, scoring, output, and delivery instructions live in `references/`.

## License

MIT License. See [LICENSE](LICENSE).
