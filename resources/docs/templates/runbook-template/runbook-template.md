## Runbook: [Procedure Name]

### Metadata

| Field | Value |
| ----- | ----- |
| **Owner** | @team or @person |
| **Severity** | P1 / P2 / P3 |
| **Frequency** | On-demand / Daily / Weekly |
| **Last Updated** | YYYY-MM-DD |

### Purpose

One-sentence description of what this runbook does and when to use it.

### Prerequisites

- [ ] Access to [system/tool]
- [ ] Permissions: [required roles]
- [ ] Alerts/monitoring: [relevant dashboards]

### Procedure

#### Step 1: [Action]

```bash
# Command or script to execute
```

**Expected result**: Describe what success looks like.
**Rollback**: How to undo this step if something goes wrong.

#### Step 2: [Action]

```bash
# Command or script to execute
```

**Expected result**: Describe what success looks like.

### Verification

- [ ] Check [metric/endpoint] returns [expected value]
- [ ] Confirm [log/alert] shows [pattern]
- [ ] Notify [stakeholder] that procedure is complete

### Troubleshooting

| Symptom | Cause | Solution |
| ------- | ----- | -------- |
| Error X | Y isn't running | Restart Y via `command` |
| Timeout | Network latency | Retry after 30s |

### Post-Incident Actions (if applicable)

- [ ] Update status page
- [ ] Write [incident postmortem](/docs/incident-postmortem-template/)
- [ ] Create follow-up tickets
- [ ] Update this runbook if the procedure changed

### Escalation

If this runbook doesn't resolve the issue within [timeframe], escalate to:

- **L2**: @on-call-engineer
- **L3**: @engineering-manager
- **External**: [vendor support link/number]

---

