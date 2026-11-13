# GraphQL Federation Onboarding Template — Companion Code

Runnable skeletons that accompany the
[GraphQL Federation Onboarding Template](https://stackpractices.com/docs/graphql-federation-onboarding-template/)
on StackPractices. They mirror the code blocks in the doc so you can copy a
working starting point instead of assembling the pieces yourself.

## Contents

```text
subgraphs/
  products/          Products subgraph (owns Product + Category entities)
    products.graphqls  SDL schema with @key, @shareable, DateTime scalar
    resolvers.js       Query/Mutation resolvers + __resolveReference with DataLoader
    server.js          Apollo Server + buildSubgraphSchema standalone server
  reviews/           Reviews subgraph (extends Product from products)
    reviews.graphqls   extend type Product with @external key
    resolvers.js       Extended-field resolvers + Review entity resolver
gateway/
  index.js           ApolloGateway + serviceList + context
  authenticated-data-source.js  RemoteGraphQLDataSource forwarding user/correlation headers
supergraph.yaml      rover supergraph compose config for all four subgraphs
tests/
  product-entity.test.js  __resolveReference + DataLoader batching tests (vitest)
```

## Usage

Install the subgraph dependencies:

```bash
npm install @apollo/server @apollo/subgraph graphql dataloader
npm install --save-dev vitest
```

Run the tests:

```bash
npx vitest run tests/
```

Compose the supergraph locally (requires [Rover](https://www.apollographql.com/docs/rover)):

```bash
rover supergraph compose --config supergraph.yaml > supergraph-schema.graphql
```

The `users` and `orders` subgraphs in `supergraph.yaml` are placeholders —
replace them with your own services or remove the entries while experimenting.

## Notes

- `createDataSources`, `authenticateUser`, and the `db` objects referenced in
  `server.js`/`resolvers.js` are intentionally left to your data layer; the
  tests show minimal fakes for them.
- Federation version is pinned to `=2.0.0` in `supergraph.yaml`. Keep the Rover
  version in CI aligned with it.
