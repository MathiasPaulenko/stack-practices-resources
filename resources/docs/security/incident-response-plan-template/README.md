# Incident Response Plan Template — Companion Resources

Companion files for [Incident Response Plan Template](https://stackpractices.com/docs/incident-response-plan-template/) on StackPractices.

## Files

| File | Purpose |
|------|---------|
| `incident-response-plan-template.md` | Blank fillable plan — severity matrix, IR team roster, six-phase lifecycle, communication plan, regulatory deadlines, metrics, tabletop exercises |
| `incident-response-plan-template.es.md` | La misma plantilla en español |

## How to use it

1. Copy `incident-response-plan-template.md` into your team's documentation repository.
2. Fill in the roster first — real names, phones, and backups — then call the numbers once to verify them.
3. Adjust the severity thresholds to your environment (a hospital, a bank, and a two-person startup classify differently).
4. Wire up the plumbing: incident Slack channel, status page, paging integration — before the next incident.
5. Run a tabletop exercise within 30 days and fix whatever breaks. An untested plan is a hypothesis.

## Customization points

- **Severity matrix**: shift rows up or down to match your blast radius definitions.
- **External contacts**: add your forensics retainer, cyber insurer, and outside counsel if you have them.
- **Regulatory table**: replace the US state-law row with the regimes that actually apply; contractual customer deadlines are usually tighter than legal ones.
- **Lifecycle tables**: keep the phases, adapt the durations to your on-call reality.
