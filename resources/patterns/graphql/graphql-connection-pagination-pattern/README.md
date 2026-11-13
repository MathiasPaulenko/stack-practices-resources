# GraphQL Connection Pagination Pattern

Runnable companion examples for the StackPractices pattern
[GraphQL Connection Pagination Pattern](https://stackpractices.com/patterns/graphql-connection-pagination-pattern/).

Two resolver implementations that paginate the same 95-user in-memory table
with full `edges` / `pageInfo` / `totalCount` output:

| File | Cursor payload | What it shows |
| --- | --- | --- |
| `offset-cursor.mjs` | `base64("offset:N")` | The classic offset cursor: simple, correct, and fine for small tables. The `LIMIT + 1` trick answers `hasNextPage` without a count query. |
| `keyset-cursor.mjs` | `base64("created_at:id")` | Keyset / sort-key pagination: the cursor carries the last row's sort values so the database seeks via `WHERE (created_at, id) < ($1, $2)` instead of scanning `OFFSET` rows. |

## Requirements

- Node.js 18+. **No dependencies** — both demos are plain ESM.

## Run

```bash
node offset-cursor.mjs   # 5 pages of 20 over 95 users, cursors like b2Zmc2V0OjE5
node keyset-cursor.mjs   # same walk, cursors carry created_at + id
```

## What to look at

- Both resolvers fetch `limit + 1` rows, keep `limit`, and use the extra row to
  set `hasNextPage` — the standard way to avoid a second query.
- `mock-db.mjs` counts queries: the offset demo issues one `COUNT(*)` plus one
  page query per request, the keyset demo only needs the page query.
- The cursors are opaque base64 strings. The demos decode them the way a real
  resolver would, but nothing in the client output depends on the format.
- `hasPreviousPage` is `offset > 0` in the offset version and `after != null`
  in the keyset version — a simplification that works for forward-only feeds.

## Common extensions

- Clamp `first` to a `MAX_PAGE_SIZE` so clients can't pull the whole table.
- Backward pagination (`last`/`before`) mirrors the forward path: read the
  page in reverse order, then flip it back.
- For many-to-many fields (user → posts → tags), paginate through the join
  table and keep the same connection shape.
