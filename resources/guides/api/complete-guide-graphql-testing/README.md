# Complete Guide to GraphQL Testing — Companion Resources

Runnable test layout for the guide
[Complete Guide to GraphQL Testing](https://stackpractices.com/guides/complete-guide-graphql-testing/).

## Contents

| File | Purpose |
| --- | --- |
| `src/typeDefs.js`, `src/resolvers.js` | Minimal schema under test |
| `tests/unit/user.resolver.test.js` | Resolver unit tests with injected context |
| `tests/integration/schema.test.js` | `graphql()` execution through the schema |
| `tests/contract/persisted-operations.test.js` | Persisted ops validate against candidate schema |
| `tests/helpers/mock-context.js` | Shared mock context factory |
| `package.json` | Layered scripts: `test:unit`, `test:integration`, `test:e2e` |

## Usage

```bash
npm install
npm run test:unit
npm run test:integration
```
