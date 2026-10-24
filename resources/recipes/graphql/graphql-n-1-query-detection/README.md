# GraphQL N+1 Query Detection — Runnable Detector

Runnable version of the StackPractices recipe
[Detect and Fix N+1 Queries in GraphQL Resolvers](https://stackpractices.com/recipes/graphql-n-1-query-detection/).

Apollo Server 4 project that counts database queries per request through an
instrumented client, warns on N+1 suspects inside `willSendResponse`, and fixes
the pattern with request-scoped DataLoader batching over an in-memory store.

## Files

| File | Purpose |
| --- | --- |
| `src/instrumented.ts` | Proxy wrapper that records every DB call into a `QueryLog`. |
| `src/queryLogger.ts` | Apollo plugin that reads the count from `contextValue` in `willSendResponse`. |
| `src/loaders.ts` | `createUserLoader` — a per-request DataLoader for authors. |
| `src/resolvers.ts` | Schema + resolvers, with the naive N+1 resolver commented out. |
| `src/server.ts` | Wires a fresh `QueryLog`, instrumented client, and loaders per request. |

## Usage

```bash
npm install
npm start
```

Open `http://localhost:4000` and run:

```graphql
query {
  posts {
    id
    title
    author {
      name
    }
  }
}
```

With the batched resolver, the operation issues 2 queries. Swap in the
commented naive resolver in `src/resolvers.ts` to see the `[N+1 SUSPECT]`
warning report 21 queries.
