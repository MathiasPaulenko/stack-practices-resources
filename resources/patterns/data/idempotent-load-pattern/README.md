# Idempotent Load Pattern — Companion Files

Runnable pieces for the pattern
[Idempotent Load: Re-run Data Loads Safely Without Duplicates](https://stackpractices.com/patterns/idempotent-load-pattern/):
an upsert statement and a self-contained Python demo you can run twice.

## Files

| File | What it does |
| --- | --- |
| `idempotent_upsert.sql` | Canonical MERGE upsert: matched rows update, new rows insert, re-runs change nothing. |
| `idempotent_load.py` | Self-contained SQLite demo of the full pattern: load-ID history check, upsert, transactional record. Running the same batch twice prints `skipped`; a changed batch upserts without duplicating. |

## Run

```bash
python idempotent_load.py   # no dependencies — stdlib sqlite3 only
```
