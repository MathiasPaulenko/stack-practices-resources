# On-Call Handoff Report

## Handoff Metadata

| Field | Value |
|-------|-------|
| Outgoing engineer | Alex |
| Incoming engineer | Dana |
| Handoff date/time | 2026-10-09 18:00 UTC |
| Shift duration | 24h → 12h coverage |

## 1. Active Incidents

### Incident #1: Payment API 500s after deploy

| Field | Value |
|-------|-------|
| Status | Mitigated (rollback done, monitoring) |
| Severity | P2 |
| Start time | 14:35 UTC |
| Incident channel | #inc-payment-500s |
| Current owner | Dana (takes over) |

**Summary:**
Checkout errors spiked to 12% after deploy 4f2a1c added a query without
an index on the orders table. Rolled back at 15:20; error rate returned
to baseline (0.3%) by 15:40. Index is building now on the shadow table.

**Next steps:**

- [ ] Verify index build finished (ETA ~18:00 UTC, owner: Dana)
- [ ] Re-deploy 4f2a1c once index is confirmed (owner: Dana, tomorrow AM)
- [ ] Post incident summary in #inc-payment-500s before EOD (owner: Dana)

**Runbook / Reference:**
docs/deploy-rollback-procedure.md — sections 2 and 4 used.

## 2. Ongoing Alerts & Warnings

| Alert | Status | First Seen | Notes |
|-------|--------|------------|-------|
| High latency on API p95 | WARN | 2h ago | Correlates with the deploy, watch it |
| Disk usage > 80% (db-03) | WARN | 1d ago | Cleanup cron runs tonight at 02:00 |
| Replication lag > 5s | OK | Resolved | Auto-resolved after index rebuild |

## 3. System Health Summary

| Component | Status | Notes |
|-----------|--------|-------|
| API latency p95 | Degraded | 890ms, was 420ms before deploy — improving since rollback |
| Error rate | Healthy | 0.3% and flat for 2h |
| Database connections | Healthy | 340/500 pool |
| Queue depth | Healthy | 1.2k normal for this hour |
| Cache hit rate | Degraded | 78%, was 91% — related to rollback cache flush, recovering |
| Disk usage | Degraded | db-03 at 81%, cleanup scheduled |

## 4. Changes & Deployments

### Completed This Shift

| Change | Time | Status | Impact |
|--------|------|--------|--------|
| Deploy 4f2a1c (payments query) | 14:30 UTC | Rolled back | Caused the P2, see incident #1 |
| Config update for caching | 14:30 UTC | Success | Partially flushed by rollback |

### Scheduled Next Shift

| Change | Time | Risk | Prepared? |
|--------|------|------|-----------|
| Kubernetes node upgrade | 06:00 UTC tomorrow | Medium | Rollback tested, platform team aware |
| SSL certificate renewal | 10:00 UTC | Low | Auto-renewal configured |

## 5. Known Issues & Workarounds

| Issue | Workaround | Ticket | Priority |
|-------|------------|--------|----------|
| Memory leak in worker process | Restart every 6h, next at 20:00 | INC-123 | Medium |
| Flaky test blocking CI retries | Retry failed job manually | DEV-456 | Low |

## 6. Escalation Paths

| Scenario | Escalate To | Contact |
|----------|-------------|---------|
| P1 incident > 30 min | Engineering Manager | Slack then phone |
| Payment errors recur | Payments TL (Priya) | PagerDuty rotation |
| Security incident | Security Team | PagerDuty |
| db-03 disk hits 90% | DBA on-call | PagerDuty |

## 7. Access & Environment Check

- [x] Dana confirmed on PagerDuty rotation for this week
- [x] VPN and production access verified last Tuesday
- [x] Dashboards and deploy tools reachable
- [ ] #inc-payment-500s joined — invite sent at 17:55, confirm
- [x] Dana is UTC+1 tonight

## 8. Notes & Context

**Unusual observations this shift:**

- Cache hit rate dipped 91%→78% after the rollback flush. Expected to
  recover by ~19:00. If it doesn't, suspect the config update.

**Requests from other teams:**

- Support ticket #4521 (billing delay complaints) is related noise from
  the incident, not a separate bug. Reply template in the ticket.

**General reminders:**

- Platform team deploy freeze starts Friday; the re-deploy of 4f2a1c
  must go out tomorrow morning or wait until Monday.
