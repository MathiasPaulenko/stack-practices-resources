# Alert Runbook: `<Alert Name>`

## Alert Metadata

| Field | Value |
|-------|-------|
| Alert Name | |
| Severity | |
| Alert Source | |
| Alert Query | |
| Trigger Condition | |
| Routing | |
| Runbook Owner | |
| Last Reviewed | |
| Last Updated | |

## Impact Assessment

| User Impact | Business Impact |
|-------------|-----------------|
| | |
| | |
| | |

## Triage (0-2 minutes)

### Step 1: Acknowledge the Alert

- [ ] Acknowledge in <paging tool> within 2 minutes
- [ ] Post in `#<incident-channel>` Slack channel: "Investigating <Alert Name>"
- [ ] Check if this is a known false positive (check recent alert history)

### Step 2: Assess Severity

| Question | If Yes |
|----------|--------|
| Is <metric> above <critical threshold>? | Escalate to P0, page secondary on-call |
| Is this during peak hours? | Higher priority — impact is greater |
| Are there related alerts firing? | Check for cascade — may be a shared dependency |
| Is this a new deployment? | Check #deployments channel for recent release |
| Is this a known maintenance window? | Check #maintenance channel |

### Step 3: Quick Checks

| Check | How | Expected |
|-------|-----|----------|
| Service health | `curl <health-endpoint>` | 200 OK |
| Recent deployment | Check `#deployments` channel | Last deploy > 30 min ago |
| Dependency status | <status-check-command-or-url> | Normal |
| Error logs | `<log-command>` | Look for repeated error patterns |

## Diagnosis (2-15 minutes)

### Step 4: Identify Error Type

| Error Pattern | Likely Cause | Next Step |
|---------------|-------------|-----------|
| <symptom A> | <cause A> | Go to Step 5A |
| <symptom B> | <cause B> | Go to Step 5B |
| <symptom C> | <cause C> | Go to Step 5C |

### Step 5A: <Cause A>

1. <diagnostic command or check>
2. <diagnostic command or check>
3. <action if confirmed>
4. <verification step>

### Step 5B: <Cause B>

1. <diagnostic command or check>
2. <diagnostic command or check>
3. <action if confirmed>
4. <verification step>

### Step 5C: <Cause C>

1. <diagnostic command or check>
2. <diagnostic command or check>
3. <action if confirmed>
4. <verification step>

## Mitigation (5-30 minutes)

### Quick Mitigation Options

| Option | When to Use | Impact | Reversibility |
|--------|-------------|--------|---------------|
| <mitigation 1> | <when> | <impact> | <how to undo> |
| <mitigation 2> | <when> | <impact> | <how to undo> |
| <mitigation 3> | <when> | <impact> | <how to undo> |

## Escalation

| Level | Who | When to Escalate |
|-------|-----|------------------|
| 1 | On-call engineer | Alert received |
| 2 | Secondary on-call | No progress after 15 minutes |
| 3 | Team lead + SRE | No progress after 30 minutes |
| 4 | Engineering manager | Incident > 1 hour or major revenue impact |
| 5 | CTO + VP Engineering | Incident > 4 hours or public impact |

### Escalation Contacts

| Role | Primary | Secondary |
|------|---------|-----------|
| <team> On-Call | | |
| SRE On-Call | | |
| <specialist> | | |
| Engineering Manager | | |

## Resolution

### Step 6: Verify Resolution

- [ ] <metric> back to normal for 10 consecutive minutes
- [ ] No new related alerts firing
- [ ] <service indicator> back to normal
- [ ] No user complaints in #support channel
- [ ] All components healthy and stable

### Step 7: Document

- [ ] Update incident in <paging tool> with resolution summary
- [ ] Post resolution in `#<incident-channel>`: "Resolved: <Alert Name> — <brief summary>"
- [ ] Create postmortem document if P1 (within 48 hours)
- [ ] File follow-up tickets for root cause fix
- [ ] Update this runbook with any new learnings

## Post-Incident

### Postmortem Required?

| Severity | Postmortem Required | Due Date |
|----------|-------------------|----------|
| P0 | Yes, blameless postmortem | Within 48 hours |
| P1 | Yes, blameless postmortem | Within 48 hours |
| P2 | Optional, if recurring | Within 1 week |
| P3 | No | N/A |

### Follow-Up Actions

| Action | Owner | Due Date | Status |
|--------|-------|----------|--------|
| Fix root cause | | | |
| Add monitoring for root cause | | | |
| Update runbook with new learnings | | | |
| Add test to prevent regression | | | |
