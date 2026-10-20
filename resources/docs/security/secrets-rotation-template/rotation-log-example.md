# Rotation Log — DB_MASTER_PASSWORD — 2026-10-15

| Field | Value |
|-------|-------|
| Secret | `DB_MASTER_PASSWORD` |
| Type | Password |
| Environment | Production |
| Storage | HashiCorp Vault |
| Old version | `v3` (`app_user_2026q3`) |
| New version | `v4` (`app_user_2026q4`) |
| Procedure | Dual-read, zero downtime |
| Window | 2026-10-15 02:00 UTC (low traffic) |
| Owner | @db-owner |
| Reviewer | @security-owner |

## Timeline

- 01:30 — New user `app_user_2026q4` created with identical grants; validated in staging
- 02:00 — Secret updated in Vault; rolling restart started
- 02:12 — Rolling restart finished
- 02:20 — `pg_stat_activity`: 0 connections on `app_user_2026q3`
- 02:25 — Reporting dashboard confirmed reading via analytics replica (separate credential — unaffected)

## Post-rotation

- 2026-10-17 — Old user dropped after 48h clean. No auth failures in logs.
- Inventory updated: last rotated `2026-10-15`, next rotation `2027-01-13`.

## Notes

- The batch ETL job uses a separate credential (`etl_user`) — confirmed not affected.
- Next rotation should try the automated script instead of manual steps.
