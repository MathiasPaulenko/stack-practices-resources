# LLM Incident Response Runbook

Fill in every `[placeholder]` before adding this to your on-call rotation.
Severity model adapted from Google SRE incident management.

## Severity levels

| Level | Criteria | Response |
|-------|----------|----------|
| SEV-1 | Service down, user harm, cost > 10x daily, data leak | Immediate, page on-call + management |
| SEV-2 | Errors +20%, latency > 5x, one feature broken, cost > 3x | Page on-call within 15 min |
| SEV-3 | Errors < 20%, intermittent < 5%, non-critical feature | Notify during business hours |
| SEV-4 | Cosmetic issues, edge-case hallucinations | Create ticket |

## Escalation path

```text
On-call engineer → (15 min, SEV-1/2) → AI team lead
  → (30 min) → Engineering manager → (SEV-1) → CTO
  → (user harm / data leak) → Legal / PR / Security
```

## Contacts

| Role | Primary | Secondary |
|------|---------|-----------|
| On-call engineer | [#channel] | [pager-service] |
| AI team lead | [lead-email] | [lead-backup] |
| Eng manager | [manager-email] | #engineering |
| Security team | [security-email] | #security-urgent |

## Incident playbooks

### 1. Model API outage

Confirm: 5xx on all calls, provider status page shows outage.
Diagnose: `check-llm-status.sh` — polls status endpoints and tests API keys.
Recover: enable `FALLBACK_MODEL` flag → cached responses → static fallbacks → disable non-critical AI features. Restore traffic 10% → 50% → 100%.

### 2. Hallucination event

Confirm: user reports + faithfulness score drop.
Diagnose: diff prompt versions, check corpus recency, compare outputs to golden set.
Recover: roll back prompt version → disable affected feature → add queries to test set.

### 3. Cost spike

Confirm: daily cost > 3x (SEV-2) or > 10x (SEV-1).
Diagnose: group cost logs by feature / user / model; look for retry loops.
Recover: enable cost throttle → rate-limit top spenders → disable non-critical features → revert expensive model.

### 4. Safety failure

Confirm: restricted action executed, harmful output, injection bypass, PII leak.
Diagnose: capture full conversation log, check guardrail state, classify attack pattern.
Recover: disable feature → block user → preserve logs → notify security/legal. PII leak: identify scope, notify affected users and DPO.

### 5. Quality degradation

Confirm: satisfaction scores down, error rate up, accuracy drop.
Diagnose: check recent prompt/model/corpus/config changes; run golden test set.
Recover: roll back the offending change → fall back to previous model → fix corpus docs → rebuild index.

## Post-incident checklist

```text
[ ] Incident documented in tracker
[ ] Timeline recorded
[ ] Root cause identified
[ ] Fix deployed and verified
[ ] Test set updated with regression cases
[ ] Monitoring thresholds adjusted
[ ] Postmortem scheduled within 48h
[ ] Action items assigned with deadlines
[ ] Stakeholders notified
[ ] This runbook updated with new learnings
```
