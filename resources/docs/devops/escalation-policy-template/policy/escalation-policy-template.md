# Escalation Policy: `<Team / Service>`

> Owner: `@name` · Review date: `YYYY-MM-DD` · Version: `1.0`

## 1. Severity Levels

| Level | Name | Criteria | Response Time | Resolution Target |
|-------|------|----------|---------------|-------------------|
| SEV 1 | Critical | Service down; data loss; security breach; revenue impact | 5 min | 4 hours |
| SEV 2 | Major | Major capability broken; major performance degradation | 15 min | 8 hours |
| SEV 3 | Minor | Feature degraded; partial outage affecting subset of users | 1 hour | 24 hours |
| SEV 4 | Low | Cosmetic issue; documentation error; non-urgent question | 4 hours | Next business day |

## 2. On-Call Roster

| Role | Primary | Backup | Contact Method | Response SLA |
|------|---------|--------|----------------|--------------|
| L1 — On-Call Engineer | `@name` | `@name` | Pager / SMS | 5 min (SEV 1), 15 min (SEV 2) |
| L2 — Team Lead | `@name` | `@name` | Phone / Slack | 15 min (SEV 1), 30 min (SEV 2) |
| L3 — Engineering Manager | `@name` | `@name` | Phone | 30 min (SEV 1), 1 hour (SEV 2) |
| L4 — VP Engineering / CTO | `@name` | `@name` | Phone | 1 hour (SEV 1 only) |

## 3. Escalation Paths

### SEV 1 — Critical

| Time Elapsed | Action | Escalate To |
|--------------|--------|-------------|
| 0 min | Acknowledge page; begin response | L1 |
| 10 min | No meaningful progress; page backup | L2 |
| 20 min | No resolution path identified; page manager | L3 |
| 45 min | No resolution; executive awareness required | L4 |
| 2 hours | Open war room; notify customer-facing teams | L3 + Comms |

### SEV 2 — Major

| Time Elapsed | Action | Escalate To |
|--------------|--------|-------------|
| 0 min | Acknowledge; assess scope | L1 |
| 30 min | No clear fix; engage team lead | L2 |
| 1 hour | No resolution; manager awareness | L3 |
| 3 hours | Open bridge; customer communication if user-facing | L3 + Comms |

### SEV 3 / SEV 4

| Time Elapsed | Action | Escalate To |
|--------------|--------|-------------|
| 0 min | Acknowledge; triage | L1 |
| 4 hours (SEV 3) | No progress; team lead notification | L2 |
| Next business day (SEV 4) | Standard backlog assignment | L2 |

## 4. Communication Channels

| Severity | Initial Alert | Updates | Status Page | Customer Comms |
|----------|---------------|---------|-------------|----------------|
| SEV 1 | Page + Slack #incidents | Every 15 min | Yes, immediately | Yes, within 30 min |
| SEV 2 | Page + Slack #incidents | Every 30 min | Yes, within 30 min | Yes, if user-facing |
| SEV 3 | Slack #incidents | Every 1 hour | No | No |
| SEV 4 | JIRA / Linear ticket | Daily standup | No | No |

## 5. Response Runbook Checklist

- [ ] Acknowledge alert within SLA
- [ ] Classify severity using criteria above
- [ ] If SEV 1 or SEV 2: create Slack #incidents thread
- [ ] If SEV 1: open war room bridge immediately
- [ ] Document timeline in incident tracking tool
- [ ] Update status page for SEV 1–2 within SLA
- [ ] Notify customer-facing teams if user impact > 5%
- [ ] Post initial assessment in incident thread within 15 minutes
- [ ] Update incident thread every 15–30 minutes until resolved

## 6. Unresponsive Responder Rules

- If the primary does not acknowledge within `5` min (SEV 1) / `10` min (SEV 2), the paging tool escalates to the backup automatically.
- If the backup does not acknowledge within the next window, escalate to L2.
- Never wait for a human to "maybe check their phone" — the chain is fully automated.

## 7. Maintenance

- Quarterly synthetic page drill (see `checklists/escalation-drill.md`).
- Contact data verified at every drill and after every team change.
- Post-incident reviews feed rule changes back into this document.
