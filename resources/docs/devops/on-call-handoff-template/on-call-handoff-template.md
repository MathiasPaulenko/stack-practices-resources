# On-Call Handoff Report

## Handoff Metadata

| Field | Value |
|-------|-------|
| Outgoing engineer | ______ |
| Incoming engineer | ______ |
| Handoff date/time | ______ |
| Shift duration | ______ |

## 1. Active Incidents

### Incident #1: `<Title>`

| Field | Value |
|-------|-------|
| Status | Investigating / Mitigated / Resolved |
| Severity | P1 / P2 / P3 / P4 |
| Start time | ______ |
| Incident channel | ______ |
| Current owner | ______ |

**Summary:**
One-paragraph description of what happened, what has been tried, and current state.

**Next steps:**

- [ ] Action item 1 (owner: ______, deadline: ______)
- [ ] Action item 2 (owner: ______, deadline: ______)

**Runbook / Reference:**
Link to relevant runbook or troubleshooting guide.

---

### Incident #2: `<Title>`

(Same structure as above)

## 2. Ongoing Alerts & Warnings

| Alert | Status | First Seen | Notes |
|-------|--------|------------|-------|
| ______ | WARN / OK | ______ | ______ |

## 3. System Health Summary

| Component | Status | Notes |
|-----------|--------|-------|
| API latency p95 | Healthy / Degraded / Critical | Current value: ______ |
| Error rate | Healthy / Degraded / Critical | Current value: ______ |
| Database connections | Healthy / Degraded / Critical | Current value: ______ |
| Queue depth | Healthy / Degraded / Critical | Current value: ______ |
| Cache hit rate | Healthy / Degraded / Critical | Current value: ______ |
| Disk usage | Healthy / Degraded / Critical | Current value: ______ |

## 4. Changes & Deployments

### Completed This Shift

| Change | Time | Status | Impact |
|--------|------|--------|--------|
| ______ | ______ | ______ | ______ |

### Scheduled Next Shift

| Change | Time | Risk | Prepared? |
|--------|------|------|-----------|
| ______ | ______ | ______ | ______ |

## 5. Known Issues & Workarounds

| Issue | Workaround | Ticket | Priority |
|-------|------------|--------|----------|
| ______ | ______ | ______ | ______ |

## 6. Escalation Paths

| Scenario | Escalate To | Contact |
|----------|-------------|---------|
| ______ | ______ | ______ |

## 7. Access & Environment Check

- [ ] Incoming engineer is on the PagerDuty/Opsgenie rotation
- [ ] VPN and production access verified this week
- [ ] Dashboards, log viewers, and deploy tools reachable
- [ ] Incident Slack channels joined and unmuted
- [ ] Physical location / timezone noted for the shift

## 8. Notes & Context

**Unusual observations this shift:**

- Any anomalies that don't rise to alert level but could be precursors to issues

**Requests from other teams:**

- Any non-urgent asks that came in during the shift

**General reminders:**

- Any team-specific context the incoming engineer should know
