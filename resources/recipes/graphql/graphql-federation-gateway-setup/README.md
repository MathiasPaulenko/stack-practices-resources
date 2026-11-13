# GraphQL Federation Gateway — Two-Subgraph Runnable Demo

Runnable companion for the recipe [Set Up a GraphQL Federation Gateway with Apollo](https://stackpractices.com/recipes/graphql-federation-gateway-setup/).

## What it demonstrates

- Two real subgraphs with `buildSubgraphSchema`: users owns `User @key`, posts extends `User` with `@external`
- `IntrospectAndCompose` supergraph composition at gateway startup
- A live cross-subgraph query: `posts { author { name posts } }` resolves `name` through an `_entities` call to the users subgraph and `posts` back on the posts subgraph
- `__resolveReference` entity resolution in action

## Run

```bash
npm install
npm start
```

The demo starts users on :4001, posts on :4002, and the gateway on :4000, executes the federated query, prints the stitched JSON response, and verifies `author.name` came from the users subgraph.

## Files

| File | Purpose |
| --- | --- |
| `src/users-service.ts` | Subgraph owning `User` with `__resolveReference` |
| `src/posts-service.ts` | Subgraph owning `Post`, extending `User` via `@extends`/`@external` |
| `src/gateway.ts` | `ApolloGateway` + `IntrospectAndCompose` + context |
| `src/demo.ts` | Boots all three services, runs the federated query, prints proof |
