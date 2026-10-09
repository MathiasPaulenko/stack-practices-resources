# Data Migration Guide — Companion Code

Runnable companion for the [data migration guide](https://stackpractices.com/guides/data-migration-guide/) on StackPractices.

## Files

| File | What it shows |
|------|---------------|
| `backfill_demo.py` | End-to-end demo on in-memory sqlite: dual-write, resumable backfill with checkpoints, idempotent re-runs, count + field-level validation |
| `schema-evolution.sql` | Expand-contract for columns and a table split with a dual-write trigger (PostgreSQL) |
| `migration-plan-template.md` | Fill-in migration plan: phases, validation checklist, rollback plan |

## Run

```bash
python backfill_demo.py
# → dual-write created user 21 in both tables
# → backfill migrated 20 rows
# → backfill migrated 0 rows   (second run is a no-op — idempotency)
# → validation passed: 21 rows, 0 mismatches
# → data-migration-guide demo OK
```

`schema-evolution.sql` targets PostgreSQL — run it against a scratch database to see the trigger keep `users` and `user_profiles` in sync.
