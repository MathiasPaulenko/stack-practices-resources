# GraphQL API with Apollo Server — Companion

Runnable Apollo Server + TypeScript project matching the recipe
[Build a GraphQL API with Apollo Server and TypeScript](https://stackpractices.com/recipes/graphql-apollo-server/).

## What's inside

| File | Purpose |
| --- | --- |
| `src/schema.ts` | Schema-first typeDefs including the `@auth` directive |
| `src/resolvers.ts` | Query/Mutation/field resolvers typed against the context |
| `src/context.ts` | Per-request context factory: auth + request-scoped DataLoader |
| `src/auth.ts` | `@auth` directive implementation via `mapSchema` |
| `src/db.ts` | In-memory `users`/`posts` store and a stub `verifyToken` |
| `src/server.ts` | Standalone Apollo Server on port 4000 |

## Run it

```bash
npm install
npm run dev
```

Then open `http://localhost:4000/` and try:

```graphql
query {
  posts {
    title
    author { name }
  }
}
```

`Post.author` resolves through the request-scoped DataLoader, so listing
fifty posts still costs one user query.

## Authenticated mutation

Send a `demo` bearer token (see `verifyToken` in `src/db.ts`):

```graphql
mutation {
  createPost(title: "New post", content: "Body") {
    id
    author { name }
  }
}
```

```bash
curl -X POST http://localhost:4000/ \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer demo' \
  -d '{"query":"mutation { createPost(title: \"New post\", content: \"Body\") { id } }"}'
```

Without the header the `@auth` directive returns `Unauthorized`.

## Notes

- `verifyToken` is a stub: `"demo"` maps to the seeded `u1` user. Swap it
  for real JWT/session verification.
- `db` is in-memory; replace it with your ORM or driver of choice. The
  resolver signatures stay the same.
