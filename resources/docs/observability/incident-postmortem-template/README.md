# Incident Postmortem Template — Companion Resources

Companion files for [Incident Postmortem Template](https://stackpractices.com/docs/incident-postmortem-template/) on StackPractices.

## Files

| File | Purpose |
|------|---------|
| `incident-postmortem-template.md` | Blank fillable template — summary, impact, timeline, five whys, action items, lessons learned |
| `example-filled.md` | The template filled with the worked P0 payment outage example from the article |

## How to use

1. Copy `incident-postmortem-template.md` into your incident documentation repo after the incident is resolved.
2. Fill the timeline first, from objective sources only (PagerDuty, CI/CD, monitoring, chat logs) — not from memory.
3. Work the five whys until you land on a systemic cause that, fixed, would have prevented the incident.
4. Give every action item an owner, a priority, and a due date before the meeting ends.
5. Share the draft with all engineering teams within 48 hours and compare with `example-filled.md` to calibrate depth.

Keep the postmortem blameless: systemic causes, never a person as the root cause.
