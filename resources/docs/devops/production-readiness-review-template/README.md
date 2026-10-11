# Production Readiness Review Template — Companion Resources

Companion files for [Production Readiness Review Template](https://stackpractices.com/docs/production-readiness-review-template/) on StackPractices.

## Files

| File | Purpose |
|------|---------|
| `production-readiness-review-template.md` | Blank fillable PRR checklist — 10 domains, review notes, and sign-off table |
| `example-filled.md` | The review filled for a real launch (notification service, conditional pass with tracked findings) |

## How to use

1. Copy `production-readiness-review-template.md` into your team wiki or docs repo.
2. Circulate it to reviewers at least a week before the review session.
3. Walk the 10 domains in order; a box only gets checked with evidence (dashboard link, runbook, test run).
4. Record every gap in Review Notes with risk, owner, and due date before the meeting ends.
5. Collect sign-off per role — engineering, product, security, SRE sign their own domain.
6. Decide: pass, conditional (launch with tracked gaps), or fail (fix and reschedule).
7. Move findings into your issue tracker; unassigned work is unfinished work.

Compare with `example-filled.md` to calibrate findings severity and sign-off decisions.
