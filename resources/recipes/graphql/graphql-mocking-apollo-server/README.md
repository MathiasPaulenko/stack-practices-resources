# Mock GraphQL Resolvers for Frontend Development

Companion code for [StackPractices: Mock GraphQL Resolvers](https://stackpractices.com/recipes/graphql-mocking-apollo-server/).

## Requirements

- Node.js 20+
- `@apollo/server` 4.x
- `@faker-js/faker` 8.x
- `msw` 2.x (optional, for client-side mocking)

## Files

| File | Description |
| ------ | ------------- |
| `mock-server.ts` | Basic Apollo Server with `mocks: true` |
| `custom-mocks.ts` | Custom scalar mocks (ID, String, Int, Boolean) |
| `type-mocks.ts` | Type-level mocks with faker for realistic data |
| `env-toggle.ts` | Toggle mocking by environment variable |
| `custom-scalars.ts` | Mock custom scalars (Date) and enums (Role) |
| `relay-pagination.ts` | Mock Relay-style cursor pagination |
| `msw-handlers.ts` | MSW 2.x handlers for client-side GraphQL mocking |
| `seeded-mocks.ts` | Seeded faker for reproducible snapshot tests |
| `error-mocks.ts` | Simulate error responses for UI error handling |

## Usage

```bash
npm install @apollo/server @faker-js/faker
npx tsx mock-server.ts
```

The mock server starts at `http://localhost:4000`.
