# GraphQL Schema Review Checklist — Companion Code

Runnable companion for the [GraphQL Schema Review Checklist](https://stackpractices.com/docs/graphql-schema-review-checklist/).

It automates the subset of checklist items that a parser can verify, so you can wire it into CI and keep human review for judgment calls (nullability, error contract, security config).

## What's inside

- `review.mjs` — SDL checker built on `graphql.parse`. Checks:
  - Type names in PascalCase
  - Field names in camelCase
  - `Boolean` fields starting with `is`/`has`/`can`
  - `id` fields typed as `ID`
  - Query list fields with cursor pagination args, and no `offset`
  - Mutations with verb names, a single `input` argument, and `*Payload` returns
  - Payload types exposing `userErrors`
  - Enum values in UPPER_SNAKE_CASE
  - `@deprecated` always carrying a `reason`
- `schemas/good-schema.graphqls` — a schema that passes every check
- `schemas/bad-schema.graphqls` — a schema that fails on purpose, one violation per checklist item
- `demo.mjs` — prints the review report for both schemas
- `tests/review.test.js` — verifies the good schema passes and the bad one fails each check

## Run it

```bash
npm install
npm run demo    # report for both schemas
npm test        # vitest
node review.mjs path/to/your/schema.graphqls   # check your own schema
```

Exit code is non-zero when any check fails, so it drops straight into a CI job.

## What it does NOT check

Depth/complexity limits, N+1, introspection policy, federation composition: those live in server config or need `graphql-inspector`/`rover`, as the doc's "How to verify" notes explain.
