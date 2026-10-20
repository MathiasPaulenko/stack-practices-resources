# Status Update Template

Copy this into the incident channel / status page on every update cadence (every 15–30 min for Sev1).

```markdown
**Incident:** #incident-YYYY-NNN
**Severity:** Sev[1-4]
**Started:** HH:MM UTC
**Status:** [Investigating / Identified / Monitoring / Resolved]

**Impact:** [What is broken and who is affected]
**What we know:** [Current understanding of root cause]
**What we are doing:** [Active remediation steps]
**ETA:** [Estimated time to resolution or next update]
**Workaround:** [Any available workaround for users]

Next update: HH:MM UTC
```

## Cadence by audience

| Audience | Channel | Frequency (Sev1) |
|----------|---------|------------------|
| Response team | Incident channel | Continuous |
| Internal stakeholders | #incidents or Slack | Every 15–30 min |
| Executives | Email/Slack DM | Every 30–60 min |
| Customers | Status page | Every 15–30 min |

## Principles

- Under-promise and over-deliver on ETAs.
- Don't speculate on root cause until you're confident.
- Update even if nothing has changed ("still investigating").
- Close the loop: notify when resolved, then follow up with the postmortem timeline.
