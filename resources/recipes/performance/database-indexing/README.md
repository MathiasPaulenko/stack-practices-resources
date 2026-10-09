# Database Indexing — Companion Code

Runnable SQL that pairs with the [database-indexing recipe](https://stackpractices.com/recipes/database-indexing/) on StackPractices.

## Files

| File | Contents |
|------|----------|
| `schema.sql` | `users` + `orders` demo tables |
| `indexes.sql` | The seven index types from the recipe: single-column, composite, partial, covering (INCLUDE), expression, FK, and keyset-cursor |
| `queries.sql` | `EXPLAIN ANALYZE` queries that exercise each index, plus maintenance queries (unused indexes, missing FK indexes, HOT ratio) |

## Run it

```bash
psql -d your_db -f schema.sql
psql -d your_db -f indexes.sql
# Seed some rows, then:
psql -d your_db -f queries.sql
```

PostgreSQL 14+ recommended — `INCLUDE`, generated columns, and `hypopg`-style features need it. The maintenance queries at the bottom of `queries.sql` are PostgreSQL-specific; the rest ports to MySQL 8 with small syntax changes (`EXPLAIN ANALYZE` instead of `EXPLAIN (ANALYZE, BUFFERS)`).

## What to look for

- `Seq Scan` vs `Index Scan` vs `Index Only Scan` in the query plans
- `Heap Fetches: 0` on query 5 — the covering index serving the whole query
- The plan change on query 4 when you remove `deleted_at IS NULL` from the predicate
