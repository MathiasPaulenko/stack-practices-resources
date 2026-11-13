# GraphQL Error Handling — Structured Extension Codes Demo

Runnable companion for the recipe [Structured GraphQL Errors with Extension Codes](https://stackpractices.com/recipes/graphql-error-handling-best-practices/).

## What it demonstrates

- `AppError` subclasses carrying `extensions.code` plus context (`errors`, `retryAfter`, `resource`, `requiredRole`)
- Apollo Server 4 `formatError`: deliberate errors pass through; unexpected throws arrive already normalized to `INTERNAL_SERVER_ERROR`, where the callback masks the leaked message and logs the real error via `unwrapResolverError`
- Real JSON responses for `UNAUTHENTICATED`, `FORBIDDEN`, `NOT_FOUND`, `VALIDATION_ERROR`, `CONFLICT`, and the masked internal error
- In-process execution via `server.executeHTTPGraphQLRequest` — no port binding needed

## Run

```bash
npm install
npm start
```

The demo executes seven cases against a real `ApolloServer` instance and prints the status code, error codes, and full JSON body for each one.

## Files

| File | Purpose |
| --- | --- |
| `src/errors.ts` | `ErrorCodes` enum + `AppError` base class and specialized errors |
| `src/schema.ts` | `typeDefs` + resolvers backed by an in-memory post store |
| `src/server.ts` | `ApolloServer` with the recipe's `formatError` masking |
| `src/demo.ts` | Seven request cases printed as real JSON responses |
