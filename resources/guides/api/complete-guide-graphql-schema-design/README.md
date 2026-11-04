# Complete Guide to GraphQL Schema Design — Companion Resources

Reference files for the guide
[Complete Guide to GraphQL Schema Design](https://stackpractices.com/guides/complete-guide-graphql-schema-design/).

## Contents

| File | Purpose |
| --- | --- |
| `schema.graphql` | Full SDL: interfaces, enums, connections, input/payload mutations, deprecation |
| `.graphql-schema-linterrc` | Linter rules enforcing the guide's conventions |
| `resolvers.ts` | Payload-error mutation + per-request DataLoader factory |

## Usage

- Drop `schema.graphql` into a schema-first project or use it as review material.
- Run the linter: `npx graphql-schema-linter schema.graphql`.
- `resolvers.ts` shows the two patterns the guide recommends: structured
  errors in payloads and request-scoped DataLoader batching.
