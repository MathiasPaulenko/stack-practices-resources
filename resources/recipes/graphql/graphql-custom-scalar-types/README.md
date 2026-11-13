# Custom GraphQL Scalar Types — Runnable Implementations

Runnable version of the StackPractices recipe
[Custom GraphQL Scalar Types for Dates, Emails, and JSON](https://stackpractices.com/recipes/graphql-custom-scalar-types/).

Five `GraphQLScalarType` implementations covering the three directions a
scalar must handle — `serialize` (server → client), `parseValue` (GraphQL
variable → server), and `parseLiteral` (inline AST node → server) — plus a
demo script that exercises every one of them.

## Files

| File | Purpose |
| --- | --- |
| `src/scalars/Date.ts` | ISO 8601 date scalar with `specifiedByURL` pointing at RFC 3339. |
| `src/scalars/Email.ts` | Email scalar that validates format and normalizes to lowercase. |
| `src/scalars/JSON.ts` | Pass-through JSON scalar that recursively walks `List`/`Object` AST nodes. |
| `src/scalars/URL.ts` | URL scalar that enforces `http:`/`https:` via the WHATWG `URL` parser. |
| `src/scalars/PositiveInt.ts` | Domain scalar that rejects zero, negatives, and non-integers. |
| `src/schema.ts` | SDL + resolvers map showing how scalars are registered. |
| `src/demo.ts` | Runs valid and invalid inputs through all three functions and prints results. |

## Usage

```bash
npm install
npm start        # runs the demo with tsx
npm run typecheck
```

To wire the scalars into a real server, copy the `scalars/` folder and merge
the entries of `src/schema.ts`'s `resolvers` map into your Apollo Server or
`makeExecutableSchema` setup.
