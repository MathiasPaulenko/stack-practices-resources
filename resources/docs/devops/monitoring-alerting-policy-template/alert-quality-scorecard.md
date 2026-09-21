# Alert Quality Scorecard

Score each alert quarterly: 6 criteria, 1–5 points each, 30 points maximum.

| Criterion | Score (1–5) | Notes |
|-----------|-------------|-------|
| Actionable: does the alert trigger a clear response? | | |
| Accurate: is the false-positive rate below 5%? | | |
| Timely: does the alert fire before user impact? | | |
| Routed: does it reach the team that can fix it? | | |
| Documented: is there a runbook linked? | | |
| Unique: is this alert redundant with another? | | |

## Interpretation

- **18–30** — healthy; keep it.
- **12–17** — put it on a 30-day improvement plan with a named owner (tighten the threshold, fix routing, or write the missing runbook).
- **Below 12** — delete it. An alert that isn't actionable, accurate, or routed trains the team to ignore pages.

## Review log

| Date | Alert | Score | Decision | Owner |
|------|-------|-------|----------|-------|
| | | | | |
