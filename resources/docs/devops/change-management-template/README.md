# Change Management Template — Companion

Downloadable versions of the templates in [Change Management Template](https://stackpractices.com/docs/change-management-template/).

## Files

| File | Purpose |
|------|---------|
| `change-request-template.md` | Blank change request — summary, impact analysis, risk assessment, rollback plan, approval table, execution log, and post-change checklist |
| `risk-assessment-matrix.md` | Risk level criteria (Low → Critical) mapped to the required approval gate |
| `post-change-review-template.md` | Post-change review form — execution variance, outcome checklist, issues, lessons, and follow-up actions |
| `change-request-example.md` | Fully worked example: a High-risk composite index migration with approvals, rollback plan, and execution log |

## Usage

Copy `change-request-template.md` into your change management system (Jira, Linear, Notion, or a `change-requests/` folder in the repo). Fill sections 1-4 before requesting approval, and complete sections 5-7 during and after execution.

Classify each change with `risk-assessment-matrix.md` so the approval gate matches the actual risk — Low gets a peer review, Critical gets the CAB.

## Requirements

None — plain Markdown templates.
