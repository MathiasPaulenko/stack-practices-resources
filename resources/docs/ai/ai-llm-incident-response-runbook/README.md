# LLM Incident Response Runbook — Companion Resources

Companion files for the [AI LLM Incident Response Runbook](https://stackpractices.com/docs/ai-llm-incident-response-runbook/) on StackPractices.com.

## What's included

| File | Format | Description |
|------|--------|-------------|
| `llm-incident-runbook.md` | Markdown | Standalone runbook: severity levels, escalation path, contacts table, five incident playbooks, post-incident checklist |
| `check-llm-status.sh` | Bash | Provider health check: polls status pages and tests API connectivity, exits non-zero on outage |

## Quick start

### 1. Copy the runbook

```bash
cp llm-incident-runbook.md oncall/runbooks/llm-incident-response.md
```

Fill in every `[placeholder]`: contacts, channels, pager service, and your severity thresholds.

### 2. Run the status check

```bash
export OPENAI_API_KEY=sk-...
export ANTHROPIC_API_KEY=sk-ant-...

./check-llm-status.sh
```

Each line reports `OK`, `FAIL`, or `SKIP` (when the API key env var is unset). Exit code is non-zero if any check fails — wire it into your alerting or run it first when section 3 of the runbook applies.

## Adapt before production

1. Tune the severity table to your traffic and budget headroom.
2. List which AI features are safe to disable — decide now, not during the outage.
3. Test every contact entry actually reaches a human.
