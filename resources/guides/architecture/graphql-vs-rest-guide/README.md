# GraphQL vs REST Migration — Companion Code

Runnable companion for [GraphQL vs REST — When to Choose and How to Migrate](https://stackpractices.com/guides/graphql-vs-rest-guide/).

Demonstrates the two most important numbers from the guide with a real request counter:

- **Phase 1 (proxy layer)**: naive resolvers calling REST endpoints fan out into 1 + N requests — a 10-post query costs **11 REST calls**.
- **Phase 2 (DataLoader)**: the same query costs **2 REST calls** (posts list + one `/users?ids=` batch).
- **Phase 4 (persisted queries)**: deterministic `sha256` query hash, much shorter than the query text.

## Files

| File | Purpose |
|------|---------|
| `rest-server.mjs` | Fake REST API (`/posts`, `/users`, `/users?ids=`, `/posts/:id/comments`) with a global request counter |
| `api.mjs` | Tiny fetch client for the REST API |
| `schema.mjs` | GraphQL SDL schema (`Post`, `User`, `Comment`, `Query`) |
| `resolvers.mjs` | `naiveResolvers` (N+1) and `batchedResolvers()` (DataLoader) |
| `server.mjs` | Apollo Server standalone instance, switchable between naive/batched |
| `demo.mjs` | End-to-end: runs the same query against both resolver sets and prints REST request counts |
| `tests/dataloader.test.js` | Vitest: request counts, response shape (no over-fetch), persisted-query hashing |

## Run

```bash
npm install
npm run demo   # prints naive 11 requests vs batched 2 requests
npm test       # 4 vitest checks
```

Node 20+ required (Apollo Server v5 and global `fetch`).
