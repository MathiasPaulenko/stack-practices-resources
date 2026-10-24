# Data Retention Policy Template — Companion

Fillable retention policy template plus runnable implementations:

- `retention-policy-template.md` — fill-in template (scope/roles, retention table, classification rules, deletion checklist).
- `s3-lifecycle.json` — S3 lifecycle rules: transition logs to Glacier/Deep Archive, expire temp data, version-expire user data.
- `purge.sql` — PostgreSQL scheduled purge job (sessions, soft-deleted user data, event logs) with VACUUM.

Source: https://stackpractices.com/docs/data-retention-policy-template/

Adapt every retention period to your legal basis before enforcing it — the examples are illustrative, not legal advice.
