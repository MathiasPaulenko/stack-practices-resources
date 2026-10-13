# Database Denormalization — Companion Demo

Runnable SQLite demo of the denormalization patterns from the guide
[Database Denormalization: Storage for Read Speed](https://stackpractices.com/guides/database-denormalization-guide/)
([versión en español](https://stackpractices.com/es/guides/database-denormalization-guide/)).

The guide uses PostgreSQL syntax (`SERIAL`, `GENERATED ALWAYS AS`, materialized
views). This demo adapts the same patterns to SQLite so it runs anywhere Python
does — no database server needed.

## What's inside

| File | What it shows |
|------|---------------|
| `denormalization_demo.sql` | Counter column + triggers, a stored computed column, a summary table (the SQLite stand-in for a materialized view), and the drift-check query |
| `run_demo.py` | Executes the SQL against an in-memory SQLite database and prints the results |

## Run it

```bash
python run_demo.py
```

Expected output: `posts.like_count = 2` after three likes and one unlike — the
triggers own the sync, so the stored counter always matches a fresh `COUNT(*)`
(drift = 0).

## Production notes

- In PostgreSQL, prefer `GENERATED ALWAYS AS ... STORED` for per-row derivations
  and real materialized views for aggregates — see the guide's worked scenario.
- The drift check is the piece to copy into production: recompute a sample of
  denormalized values from the source and alert on divergence.
