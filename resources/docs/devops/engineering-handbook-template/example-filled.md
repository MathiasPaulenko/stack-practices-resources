# Engineering Handbook: Nimbus Platform Team

> Last updated: 2026-11-01 | Owner: Sofia Chen (EM) | Questions: #eng-nimbus

---

## 1. Our Philosophy

### Mission
We keep Nimbus's deployment platform reliable enough that product teams never think about infrastructure.

### Principles
1. **Boring technology for core paths** — Postgres over the new database of the month; boring is debuggable at 3 a.m.
2. **Small batches** — PRs under 400 lines get reviewed in hours; thousand-line PRs get ignored for days.
3. **Write it down** — if a decision took a meeting, it takes a paragraph in the handbook or an ADR.

### What We Value
| Value | What It Looks Like | What It Does Not Look Like |
|-------|--------------------|---------------------------|
| Quality | Contract tests on every service boundary | "It worked in staging" |
| Speed | Daily deploys behind feature flags | Big-bang quarterly releases |
| Collaboration | RFCs for anything cross-team | Surprising another team in a demo |
| Ownership | The team that ships it pages for it | Filing a ticket to "infra" and walking away |

---

## 2. How We Work

### Communication
| Channel | Use For | Response Time | Notes |
|---------|---------|---------------|-------|
| Slack #eng-nimbus | Daily coordination | Same day | Threads required |
| Slack DMs | Private topics | Same day | Prefer channels |
| Email | Vendors, formal notices | 24 hours | |
| GitHub PR comments | Code discussion | During review | |
| Video call | Kickoffs, 1:1s, incidents | Scheduled | Record architecture reviews |

### Meetings
| Meeting | Frequency | Duration | Required | Purpose |
|---------|-----------|----------|----------|---------|
| Standup | Daily, async in Slack | 10 min | All | Blockers |
| Planning | Biweekly, Tue | 60 min | All | Commit to sprint |
| Retro | Biweekly, Fri | 45 min | All | Process fixes |
| 1:1 | Weekly | 30 min | Manager + IC | Growth |

### Working Hours
- Core hours: 10:00-15:00 ET
- On-call responds within 15 minutes during shifts

---

## 3. Development Workflow

1. Pick up a card from the sprint's ready column in Linear
2. Branch `feat/…` or `fix/…` off `main` (trunk-based; see branching doc)
3. Code + tests; run `make check` locally
4. Open PR with the template filled; request review from one teammate + one out-of-area reviewer for cross-cutting changes
5. Address feedback, resolve threads, merge with squash
6. Deploys automatically to staging; production deploy is a button in GitHub Actions
7. Watch the deploy dashboard for 10 minutes; close the Linear card

### Definition of Done
- [ ] Tests cover new logic (>80% on changed files)
- [ ] Approved by 1 non-author engineer
- [ ] Runbook updated if the change affects on-call
- [ ] Deployed and verified in production

### Code Review Standards
- First review within 4 working hours
- Nits prefixed "Nit:" — author decides
- Silence is not approval; ask if unclear

---

## 4. Technical Standards

| Layer | Primary | Approved Alternatives | Deprecated |
|-------|---------|----------------------|------------|
| Backend | Go 1.23 | Python (tooling only) | Node services |
| Frontend | React 18 + TypeScript | — | jQuery |
| Database | Postgres 16 | Redis for cache | MongoDB |
| Queue | SQS | — | RabbitMQ |

### Architecture Principles
1. **Services own their data** — no shared database access; see ADR-014
2. **Synchronous only when a user waits** — everything else through the queue
3. **Deployable on day one** — a new service reaches production skeleton in its first sprint

### Security
- OIDC service-to-service auth; no long-lived keys
- Secrets in AWS Secrets Manager; 90-day rotation
- `govulncheck` in CI on every PR

### Observability
- RED metrics on every endpoint; Grafana dashboard per service
- Structured JSON logs with `trace_id`
- SLOs defined before launch: 99.9% availability, p95 < 300ms

---

## 5. Operational Practices

### On-Call
- Weekly rotation, 6 engineers, handoff Mondays 10:00 ET with the handoff template
- P1 15 min / P2 30 min / P3 2 hours
- Escalates to EM after 15 min unacknowledged
- +$200/week stipend

### Deployment
- Deploy anytime; freeze during incident windows only
- Canary on the API tier (10% for 15 min)

---

## 6. Career Growth

Levels E1-E5 as per the company matrix; promotion requires sustained next-level impact over two review cycles.

---

## 7. Onboarding

### First Week
- [ ] `nix develop` environment running, first commit merged by Wednesday
- [ ] Met EM, TL, PM and onboarding buddy (assigned on day one)
- [ ] Read handbook sections 1-3 and the last two incident postmortems

### First 90 Days
| Milestone | By Day | Verified By |
|-----------|--------|-------------|
| Ships code independently | 30 | TL |
| Completes on-call shadow week | 60 | EM |
| Owns a small feature end to end | 90 | EM + PM |

---

## 8. How to Change This Handbook

Maintained by the EM. Changes go through PR to `nimbus/handbook`, discussion in #eng-nimbus, merge after TL + EM approval, announced in channel.

## Changelog

| Date | Change | Author |
|------|--------|--------|
| 2026-07-14 | Initial version | S. Chen |
| 2026-09-02 | Added canary deploy policy | R. Osei |
| 2026-11-01 | Onboarding 30-60-90 table | S. Chen |
