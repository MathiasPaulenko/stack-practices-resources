# GraphQL Schema Stitching Pattern — Companion Files

Runnable stitching example for the pattern
[GraphQL Schema Stitching Pattern](https://stackpractices.com/patterns/graphql-schema-stitching-pattern/):
two standalone GraphQL services merged behind a single gateway with
`@graphql-tools/stitch`.

## Files

| File | What it does |
| --- | --- |
| `users-service.ts` | `users-api` subschema — `User` type, `user`/`users` queries, seed data. Serves :4001 standalone. |
| `posts-service.ts` | `posts-api` subschema — `Post` type plus the `postsByAuthorIds` batch query used by the batch-delegation variant. Serves :4002. |
| `gateway.ts` | Builds executors (`@graphql-tools/executor-http`), stitches both subschemas, adds `extend type` link types, and delegates `User.posts` / `Post.author` via `delegateToSchema`. Serves :4000. |
| `client-query.graphql` | The one-request-two-services query from the pattern page, with a `curl` example. |
| `package.json` / `tsconfig.json` | Dependencies and strict TypeScript config. |

## Run

```bash
npm install
npm run users    # users-api on :4001
npm run posts    # posts-api on :4002
npm run gateway  # stitched schema on :4000
```

Then open `client-query.graphql` and run it against `http://localhost:4000/graphql`.

## Notes

- `selectionSet` is mandatory on merged fields — `User.posts` needs `{ id }` from the parent user to build the `posts(authorId:)` delegation.
- `mergeSchemas` and the old `schema-stitching` package are deprecated; `stitchSchemas` from `@graphql-tools/stitch` is the current API.
- `info` is typed `any` in the delegation resolvers for brevity — `GraphQLResolveInfo` + `mergeInfo` generics work too.
