# GraphQL Relay Cursor Pagination — Companion

Runnable companion for the [Relay Connections recipe](https://stackpractices.com/recipes/graphql-pagination-relay-connections/) on StackPractices.

## Contents

| File | What it is |
|------|------------|
| `src/schema.ts` | `PageInfo` / `PostEdge` / `PostConnection` / `PaginationInput` type definitions |
| `src/cursor.ts` | `encodeCursor` / `decodeCursor` (base64) |
| `src/resolvers.ts` | Bidirectional resolver: `first`/`after` forward, `last`/`before` backward, `take + 1` spillover |
| `src/server.ts` | Apollo Server with an in-memory store (57 seeded posts) |
| `package.json` | deps + `npm start` |

## Run it

```bash
npm install
npm start
```

Then open the printed URL and try:

```graphql
query {
  posts(pagination: { first: 5 }) {
    edges { cursor node { id title } }
    pageInfo { hasNextPage endCursor }
  }
}
```

Take the `endCursor` and pass it as `after` for the next page.

Source recipe: https://stackpractices.com/recipes/graphql-pagination-relay-connections/
