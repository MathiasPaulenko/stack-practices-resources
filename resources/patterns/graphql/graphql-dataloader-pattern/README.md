# GraphQL DataLoader Pattern

Runnable demo of the DataLoader library contract used in the [GraphQL DataLoader Pattern](https://stackpractices.com/patterns/graphql-dataloader-pattern/) article.

## What it demonstrates

`contract.mjs` exercises the five guarantees that make the pattern work:

1. **Per-tick dedup**: 4 `load()` calls with 2 unique keys produce 1 database query.
2. **Per-key errors**: an `Error` at one index rejects only that caller (`Promise.allSettled` shows `u404` failing while `u2` resolves).
3. **Cache invalidation**: after a mutation, `clear(key)` drops the stale entry; the next `load()` re-fetches.
4. **`loadMany` order**: results stay aligned with input keys, including not-found slots.
5. **`cacheKeyFn`**: object keys dedupe by value, not by reference.

`mock-db.mjs` is a fake database that counts queries and returns copies, like a real driver.

## Run

```bash
npm install
npm run demo
```

Expected output shows the dedup count, the per-key error split, `Ada` → `Ada Lovelace` after `clear()`, aligned `loadMany` results, and one batch call for two equal object keys.

## Requirements

Node.js 18+.
