# Onboarding Guide

Welcome to the team! This guide gets you from day one to your first meaningful contribution.

## Day 1: Accounts and Access

- [ ] Email and Slack/Teams account created
- [ ] Git repository access granted
- [ ] CI/CD platform access configured
- [ ] Development environment credentials received
- [ ] Calendar invites sent for standups and team rituals

## Days 1-2: Environment Setup

See your team's environment setup guide for detailed instructions.

### Required tools

| Tool | Version | Purpose | Install link |
|------|---------|---------|--------------|
| [Node.js] | [20.x] | Runtime | [nodejs.org](https://nodejs.org) |
| [Docker] | [latest] | Containers | [docker.com](https://docker.com) |
| [Git] | [2.40+] | Version control | [git-scm.com](https://git-scm.com) |

### Repository setup

```bash
git clone git@github.com:org/repo.git
cd repo
npm install
npm run dev
```

Verify: `http://localhost:4321` should show the application.

## Days 2-3: Codebase Overview

### Architecture
[High-level diagram or description of system components]

### Key directories

| Directory | Purpose |
|-----------|---------|
| `/src/components` | Reusable UI components |
| `/src/pages` | Route definitions |
| `/src/lib` | Shared utilities and schemas |
| `/tests` | Test suites |

### Conventions

- Branch naming: `feature/description`, `bugfix/description`
- Commits: [Conventional Commits](https://conventionalcommits.org)
- Style: enforced by ESLint and Prettier

## Days 3-5: First Contributions

Look for issues labeled `good first issue`, `help wanted`, or `documentation`.

| Day | Task | Goal |
|-----|------|------|
| 3 | Fix a typo or update docs | Learn the PR workflow |
| 4 | Write a unit test | Understand testing standards |
| 5 | Pick a small bug | End-to-end contribution flow |

## Week 2+: Going Deeper

- [ ] Attend the architecture overview session
- [ ] Read recent ADRs in `/docs/adr/`
- [ ] Shadow an on-call rotation (observation only)
- [ ] Pair program with a teammate

## Resources

- [Team wiki](link) · [API docs](link) · [Runbooks](link) · [ADRs](link)

## Questions?

Your onboarding buddy: **[Name]** — Slack `@username` · `name@company.com`
