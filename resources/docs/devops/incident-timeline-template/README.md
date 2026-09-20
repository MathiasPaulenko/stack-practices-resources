# Incident Timeline Template — Companion Resources

Companion files for [Incident Timeline Template](https://stackpractices.com/docs/incident-timeline-template/) on StackPractices.

## Files

| File | Purpose |
|------|---------|
| `incident-timeline-template.md` | Blank fillable template — T± notation, delay analysis table, quality checklist |
| `example-filled.md` | The template filled with the worked SEV1 example from the article (auth-service JWT rotation incident) |

## How to use

1. Copy `incident-timeline-template.md` into your postmortem doc or repo.
2. Fill the timeline during or right after the incident — every event with a timestamp and a source.
3. Run the delay analysis: each gap over 10 minutes needs an annotation and an action item.
4. Check the Quality Checklist at the bottom before publishing the timeline.
5. Compare with `example-filled.md` to calibrate granularity.

All timestamps in UTC. Prefer machine sources (metrics, alerts, CI/CD, chat) over memory.
