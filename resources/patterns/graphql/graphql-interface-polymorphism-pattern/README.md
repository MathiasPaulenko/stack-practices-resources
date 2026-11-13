# GraphQL Interface Polymorphism Pattern — Companion Code

Runnable demo of the pattern documented at
[stackpractices.com/patterns/graphql-interface-polymorphism-pattern/](https://stackpractices.com/patterns/graphql-interface-polymorphism-pattern/).

## What it shows

- `Node` and `Searchable` interfaces implemented by `Post`, `Comment`, and `User` in SDL
- Discriminator-based `__resolveType`: objects carry `__typename`, resolution is a lookup (never shape-guessing)
- Inline fragments selecting type-specific fields on an abstract return type
- A Relay-style `node(id)` lookup decoding a base64 `Type:localId` global id

## Layout

| File | Purpose |
|------|---------|
| `schema.mjs` | SDL typeDefs + seed data with `__typename` discriminators |
| `resolvers.mjs` | `__resolveType` + field resolvers + `node(id)` decode |
| `demo.mjs` | Executes a mixed-type feed query and a global-id lookup |
| `tests/polymorphism.test.mjs` | 6 tests over real graphql-js execution |

## Run

```bash
npm install
npm run demo    # prints the resolved feed + node() lookup
npm test        # 6 vitest assertions
```

Requires Node 18+.
