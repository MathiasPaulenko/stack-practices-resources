# GDPR Compliance Guide — Companion

SQL schema for the consent and DSAR tables from the guide:

- `consent_schema.sql` — `user_consents` (purpose-scoped, versioned, with withdrawal) and `dsar_requests` (type, status, SLA tracking), plus the auto-delete cron for inactive accounts.

## Usage

1. Run the schema against your Postgres database (adapt types for MySQL/SQLite).
2. Record every consent grant/withdrawal — a bare boolean is not enough for auditors.
3. Wire DSAR intake to a ticketing channel; the 30-day clock starts at receipt.

Source article: <https://stackpractices.com/guides/compliance-gdpr-guide/>
