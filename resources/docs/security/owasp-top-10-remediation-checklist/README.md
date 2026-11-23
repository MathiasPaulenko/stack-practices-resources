# OWASP Top 10 2025 — Remediation Checklist

Companion files for [OWASP Top 10 2025 Remediation Checklist](https://stackpractices.com/docs/owasp-top-10-remediation-checklist/) on StackPractices.

## Contents

- `owasp-top-10-2025-remediation-checklist.md` — all ten categories as printable tables, ordered by priority (P0 first). Copy into your issue tracker or audit workspace.
- `remediation-tracker.csv` — seed tracker with one row per P0 check. Columns: `category`, `check`, `priority`, `status`, `owner`, `evidence`, `revisit_date`, `retest_result`. Extend it with the P1/P2 items from the full checklist as needed.
- `owasp-top-10-2025-remediation-checklist.es.md` — Spanish version of the checklist.

## Usage

1. Import the CSV into Jira, Linear, GitHub Issues, or a spreadsheet.
2. Work each category top to bottom; mark `status` as `open / in progress / verified / accepted-risk`.
3. Record proof in `evidence` — the commit, regression test, or scan output that shows the fix works.
4. Re-run the relevant section after pentest findings; run the full pass quarterly.

For the runnable mitigation code (SSRF protection, access control, fail-closed handlers, pytest checks), see the sibling resource `resources/guides/security/complete-guide-owasp-top-10-2025/`.
