# On-Call Handoff Template — Companion Resources

Companion files for [On-Call Handoff Template](https://stackpractices.com/docs/on-call-handoff-template/) on StackPractices.

## Files

| File | Purpose |
|------|---------|
| `on-call-handoff-template.md` | Blank fillable handoff report — incidents, alerts, health, changes, escalation paths, access check, notes |
| `example-filled.md` | The template filled with a worked shift handoff (P2 payment API incident, rollback, pending deploy) |

## How to use

1. Copy `on-call-handoff-template.md` into your team wiki, shared drive, or incident tool.
2. Update it during the shift, not at the end — memory compresses badly under fatigue.
3. Walk the incoming engineer through it in ~20 minutes: incidents, alerts, health, changes, known issues, questions.
4. Run section 7 (access check) before sign-off — the classic failure is an incoming engineer who can't log in to anything.
5. Get explicit acknowledgment; "read it" isn't a confirmation.
6. Compare with `example-filled.md` to calibrate the level of detail.

For async handoffs across time zones, the article includes a Slack-ready short format.