# Runbook Template

Reusable Markdown runbook template for operational procedures and incident response, matching the StackPractices guide: <https://stackpractices.com/docs/runbook-template/>

## Files

- `runbook-template.md` — blank fill-in template: metadata, prerequisites, procedure steps (expected result + rollback per step), verification checklist, troubleshooting table, post-incident actions, escalation block.
- `runbook-example.md` — the same template filled in for a real scenario: a Kubernetes `PaymentServiceHighCPU` alert, with branching diagnostics and per-condition mitigations.

## Usage

1. Copy `runbook-template.md` into your `docs/runbooks/` directory (or wiki) and rename it after the procedure.
2. Fill the metadata table (owner, severity, frequency, last updated).
3. Write steps an unfamiliar executor can follow: one command per step, expected result, rollback.
4. Link the runbook URL from the alert that triggers it.

For guidance on when a procedure deserves a runbook, the two shapes (procedure vs. diagnostic), and rolling out a runbook library, read the full guide.
