# GraphQL DataLoader Batching — Companion

Runnable companion for the StackPractices recipe
[Batch and Cache Database Queries with GraphQL DataLoader](https://stackpractices.com/recipes/graphql-dataloader-batching/).

## What it contains

- `src/mock-db.ts` — in-memory `users`/`posts` tables that count every simulated database query.
- `src/loaders.ts` — `createUserLoader` (entity loader) and `createPostsByAuthorLoader` (one-to-many loader). Both return result arrays aligned to the input keys.
- `src/context.ts` — per-request context factory; a fresh DataLoader per request keeps the cache scoped.
- `src/demo.ts` — executable demo showing N+1 vs batched query counts, cache deduplication, `loadMany` alignment, per-key errors, mutation invalidation via `clear()`, and the one-to-many loader.

## Run it

```bash
npm install
npm start        # tsx src/demo.ts
npm run typecheck
```

Expected output highlights: naive resolvers issue 6 queries for 5 posts; DataLoader issues 2. Three `load('u1')` calls hit the database once. `loadMany(['u1','missing'])` returns `Ada` plus a per-key `Error`. A mutation followed by `clear('u1')` refreshes the cached entity.
