# Delivery Channels

Use this reference only when the user asks to schedule, automate, send, or push the radar.

## Principle

The Skill creates the briefing. Delivery requires a scheduler plus a message channel. Do not claim a channel is live unless the environment has the needed integration and the user has authorized it.

## ChatGPT Notification

Best for V0.

What is needed:

- A scheduled task or automation in ChatGPT/Codex
- User confirmation of cadence and time
- The Skill prompt and profile

Suggested scheduled prompt:

```text
Use $daily-ai-startup-radar to create my Daily AI Startup Radar. Use my saved Personal Lens, cover Silicon Valley, New York, Singapore, and Hong Kong, focus on the last 24 hours, and notify me only when the briefing is ready or when research cannot be completed.
```

## Lark or Feishu

Best for V1 team or personal channel delivery.

What is usually needed:

- Lark/Feishu bot or custom webhook
- Webhook URL stored securely
- Markdown or rich-text compatible output
- Optional secret/signature verification depending on bot configuration

Recommended format:

- Use the compact push template for the first message.
- Link to the full briefing if a longer version is stored elsewhere.
- Keep each company note short enough to scan on mobile.

## WhatsApp

Possible, but usually more setup than Lark.

What is usually needed:

- WhatsApp Business or Cloud API setup
- Approved sender number
- Access token and phone number ID
- Template approval for outbound notifications outside an active conversation window
- User opt-in where applicable

Recommended format:

- Top 3 only
- One short pattern
- One action
- Link to full briefing if available

## SMS

Possible, but not ideal for the full briefing.

What is usually needed:

- SMS provider such as Twilio or another messaging API
- Sender number
- User phone number and consent
- Message length management

Recommended format:

- Alert only
- Top 1-3 companies
- No long analysis

## Delivery Safety

- Ask before enabling a new outbound channel.
- Never expose webhook URLs, tokens, phone numbers, or secrets in the briefing.
- If delivery fails, explain the failure and preserve the generated briefing.
- For recurring runs, stay quiet when there is no meaningful new signal unless the user asked for a daily status regardless.
