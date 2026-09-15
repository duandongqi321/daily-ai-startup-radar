# Publishing to GitHub

This guide helps you publish Daily AI Startup Radar as a public GitHub repository.

## Before You Start

Make sure these files are public-safe:

- `SKILL.md`
- `README.md`
- `SPEC.md`
- `LICENSE`
- `CONTRIBUTING.md`
- `CHANGELOG.md`
- `agents/openai.yaml`
- `config/user_profile.example.yaml`
- `references/*.md`

Do not publish:

- `config/user_profile.yaml`
- API keys
- webhook URLs
- phone numbers
- private founder notes
- paid database exports

## Option A: GitHub Website

Use this if you prefer clicking in the browser.

1. Go to GitHub and sign in.
2. Click the `+` button in the top right.
3. Choose `New repository`.
4. Repository name: `daily-ai-startup-radar`.
5. Description: `An open-source ChatGPT Skill for personalized daily AI startup intelligence.`
6. Visibility: `Public`.
7. Do not add a README, license, or gitignore on GitHub, because this folder already has them.
8. Click `Create repository`.
9. GitHub will show commands for pushing an existing local repository. Use the commands from Option B below, replacing `YOUR_GITHUB_USERNAME`.

## Option B: Terminal

Run these commands from the Skill folder:

```bash
cd path/to/daily-ai-startup-radar
git init
git branch -M main
git add .
git status
git commit -m "Initial Daily AI Startup Radar skill"
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/daily-ai-startup-radar.git
git push -u origin main
```

Replace `YOUR_GITHUB_USERNAME` with your real GitHub username.

If Git says `remote origin already exists`, use:

```bash
git remote set-url origin https://github.com/YOUR_GITHUB_USERNAME/daily-ai-startup-radar.git
git push -u origin main
```

## Option C: GitHub CLI

Use this if you already have `gh` installed and logged in:

```bash
cd path/to/daily-ai-startup-radar
git init
git branch -M main
git add .
git commit -m "Initial Daily AI Startup Radar skill"
gh repo create daily-ai-startup-radar --public --source=. --push --description "An open-source ChatGPT Skill for personalized daily AI startup intelligence."
```

## Create a Release

After the repository is pushed:

1. Open the repository on GitHub.
2. Click `Releases`.
3. Click `Draft a new release`.
4. Tag: `v0.1.0`.
5. Title: `Daily AI Startup Radar v0.1.0`.
6. Notes:

```text
Initial V0 release of Daily AI Startup Radar.

- Daily AI startup briefing workflow
- Personal Lens onboarding
- User profile configuration template
- Research playbook
- Scoring rubric
- Daily briefing and compact push templates
```

7. Attach the public zip file if you created one.
8. Click `Publish release`.

## Verify

After publishing, check:

- GitHub shows the README correctly.
- `config/user_profile.yaml` is not in the repository.
- `config/user_profile.example.yaml` is in the repository.
- `SKILL.md` is visible at the root.
- The repository is public.
