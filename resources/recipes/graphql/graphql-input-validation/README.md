# GraphQL Input Validation — Zod Schemas at the Resolver Boundary

Runnable companion for the StackPractices recipe
[Validate and Sanitize GraphQL Input Types Server-Side](https://stackpractices.com/recipes/graphql-input-validation/).

## What's inside

- `src/schema.ts` — SDL input types (`CreatePostInput`, `UpdateUserInput`)
- `src/schemas.ts` — Zod 4 schemas plus `validateInput`, which maps `safeParse` issues to flat `{field, message}` errors
- `src/errors.ts` — `ValidationException` carrying the field errors
- `src/resolvers.ts` — mutations validating at the boundary before touching the database
- `src/server.ts` — Apollo Server 4 `formatError` with `unwrapResolverError` (required; resolver errors arrive wrapped in `GraphQLError`)
- `src/demo.ts` — exercises valid, invalid, and cross-field inputs end to end
- `tests/schemas.test.ts` — vitest suite covering transforms, error shape, cross-field `path`, and resolver behavior

## Run it

```bash
npm install
npm run demo    # node --experimental-strip-types src/demo.ts
npm test        # vitest run
```

Requires Node.js ≥ 22.6 for `--experimental-strip-types`.

## Key points

- Validate at the resolver boundary, before database access.
- `safeParse` returns data or a typed error — never throws.
- `.transform()` (trim, DOMPurify) produces sanitized output during parsing.
- Zod 4 moved ISO/format validators to top level: `z.iso.datetime()`, `z.email()`, `z.url()`.
- In Apollo Server 4, call `unwrapResolverError(error)` inside `formatError` before `instanceof` checks.
