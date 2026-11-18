# Backup Verification Test Template — Companion

Fill-in verification record plus runnable implementations:

- `backup-verification-test-template.md` — fill-in test record (identification, scope/objectives, restore procedure, validation checklist, results summary, issue log).
- `postgres-restore-verify.sh` — runnable PostgreSQL restore-and-verify script: creates a throwaway DB, restores the dump, checks row counts, constraints and indexes, runs a smoke query, then cleans up.
- `rto-rpo-worksheet.txt` — RTO/RPO measurement worksheet with a filled example (restore timeline, data-loss window, pass/fail against targets, issues and remediation).

Source: https://stackpractices.com/docs/backup-verification-test-template/

Adapt paths, hosts, and thresholds before running the script — and always restore into an isolated environment, never production.
