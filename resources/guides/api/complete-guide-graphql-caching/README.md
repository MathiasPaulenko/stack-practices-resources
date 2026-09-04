# GraphQL Caching — Companion Resource

Companion code for the StackPractices guide [Complete Guide to GraphQL Caching](https://stackpractices.com/guides/complete-guide-graphql-caching/).

## Contents

- `apollo-client-persisted-queries.js` — Apollo Client with persisted queries, GET requests, and normalized cache config.
- `dataloader-with-redis.js` — DataLoader that checks Redis first, then falls back to the database.
- `cache-invalidation.js` — Event-driven cache invalidation with Redis pub/sub and versioned cache keys.
- `apollo-client-normalized-cache.js` — Apollo Client normalized cache with mutation update helpers.
- `meta.json` — Resource metadata.

## Running

These are reference snippets, not a runnable app. Copy the relevant pattern into your Apollo Server or Apollo Client setup.

## Key concepts

- **CDN caching**: GET requests + persisted queries for consistent cache keys.
- **DataLoader**: per-request batching and caching to prevent N+1.
- **Redis**: cross-request caching with TTL and pub/sub invalidation.
- **Apollo Client**: normalized cache with mutation updates.
- **Cache invalidation**: event-driven, versioned keys, and tag-based purging.
