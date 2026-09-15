# Cursor-Based Pagination in PostgreSQL (Keyset vs OFFSET)

Runnable companion for the StackPractices recipe at <https://stackpractices.com/recipes/cursor-pagination-postgresql/>.

## Files

| File | Language | Description |
|------|----------|-------------|
| `schema.sql` | SQL | Table schema, composite indexes, partial index, generated column |
| `cursor_pagination.ts` | TypeScript | Repository with `pg` driver and base64url cursor encoding |
| `cursor_pagination.py` | Python | Async implementation with `asyncpg` |
| `CursorPagination.java` | Java | JDBC implementation with `java.util.Base64` |

## Quick start

```bash
# 1. Apply the schema
psql -d your_db -f schema.sql

# 2. TypeScript
npm install pg
npx tsx cursor_pagination.ts

# 3. Python
pip install asyncpg
python cursor_pagination.py

# 4. Java
javac CursorPagination.java
java -cp .:postgresql.jar CursorPagination
```

## How it works

1. The client requests the first page (no cursor).
2. The server queries `ORDER BY created_at DESC, id DESC LIMIT N+1`.
3. If N+1 rows are returned, `hasMore = true` and the next cursor is encoded from the Nth row.
4. The client sends the cursor on the next request.
5. The server decodes the cursor and queries `WHERE (created_at, id) < (cursor_values)`.
6. The index seek is O(log n), so deep pages are as fast as the first page.

## Key indexes

- `(created_at DESC, id DESC)` — stable ordering with tiebreaker.
- `(score DESC, id DESC)` — alternative sort by score.
- `WHERE deleted_at IS NULL` — partial index for soft-deleted rows.
