# GraphQL Batched Resolver Pattern

Runnable companion examples for the StackPractices pattern
[GraphQL Batched Resolver Pattern](https://stackpractices.com/patterns/graphql-batched-resolver-pattern/).

Three small programs that demonstrate the same resolvers against an in-memory
database that counts queries:

| File | What it shows | Queries for 50 posts + authors |
| --- | --- | --- |
| `n-plus-one.mjs` | The N+1 problem: one resolver call per post | **51** |
| `batched-resolver.mjs` | DataLoader batching with per-request loaders | **2** |
| `manual-batch.mjs` | The same pattern with a tiny hand-rolled batcher (no dependencies) | **2** |

## Requirements

- Node.js 18+
- `npm install` only needed for `batched-resolver.mjs` (pulls `dataloader`).
  The other two demos run with zero dependencies.

## Run

```bash
npm install            # once, for the DataLoader demo

node n-plus-one.mjs    # baseline: 51 queries
node batched-resolver.mjs  # DataLoader: 2 queries
node manual-batch.mjs      # manual batcher: 2 queries
```

## What to look at

- `mock-db.mjs` counts queries, so the difference between N+1 and batching is a
  number, not a claim. 50 posts share only 30 distinct authors, which also shows
  DataLoader's per-request deduplication.
- `batched-resolver.mjs` creates loaders in a `createLoaders(context)` factory,
  the same shape you would use inside an Apollo Server `context` function. The
  batch function returns results **in key order** — that positional contract is
  what makes `userMap.get(id)` mandatory.
- `manual-batch.mjs` shows the pattern's mechanics without the library: queue
  keys for one microtask window, dedupe with a `Set`, fire the batch once, map
  results back by key.

## Common extensions

- Set `maxBatchSize` when lists can reach thousands of parents.
- Return `new Error()` for individual failed keys instead of throwing.
- Call `loader.clear(id)` after a mutation writes back to the cached entity.
