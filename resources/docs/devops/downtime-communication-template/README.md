# Incident & Downtime Communication Template — Companion Resources

Companion files for [Incident & Downtime Communication Template](https://stackpractices.com/docs/downtime-communication-template/) on StackPractices.

## Files

| File | Purpose |
|------|---------|
| `downtime-communication-template.md` | Blank fillable template — metadata, audience matrix, six message blocks, severity timing table, approval checklist |
| `status-page-messages.md` | Status page copy for the full SEV 1 lifecycle (Investigating → Identified → Monitoring → Resolved) plus a SEV 3 short variant |
| `service-template-checkout.yaml` | Pre-built service template — fill two or three fields when the incident fires instead of writing from scratch |
| `example-filled.md` | The master template filled with a worked SEV 1 incident (EU login failures, 27-minute resolution) |

## How to use

1. Copy `downtime-communication-template.md` into your team wiki or incident tool.
2. Fill the audience matrix with your real channels and owners before you need it.
3. Create one `service-template-*.yaml` per top service and keep it next to the runbook.
4. During an incident: send messages in the order listed — internal alert, status page, exec summary — then update on the severity cadence.
5. Compare against `example-filled.md` to calibrate how much detail each audience gets.
6. After resolution, publish the postmortem note and fold any lessons back into the templates.
