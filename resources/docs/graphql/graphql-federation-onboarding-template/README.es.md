# Plantilla de Onboarding en GraphQL Federation — Código complementario

Esqueletos ejecutables que acompañan a la
[Plantilla de Onboarding en GraphQL Federation](https://stackpractices.com/es/docs/graphql-federation-onboarding-template/)
de StackPractices. Replican los bloques de código del documento para que puedas
copiar un punto de partida funcional en vez de armar las piezas por tu cuenta.

## Contenido

```text
subgraphs/
  products/          Subgraph de products (dueño de las entidades Product + Category)
    products.graphqls  Schema SDL con @key, @shareable, escalar DateTime
    resolvers.js       Resolvers de Query/Mutation + __resolveReference con DataLoader
    server.js          Apollo Server + servidor standalone con buildSubgraphSchema
  reviews/           Subgraph de reviews (extiende Product de products)
    reviews.graphqls   extend type Product con key @external
    resolvers.js       Resolvers de campos extendidos + entity resolver de Review
gateway/
  index.js           ApolloGateway + serviceList + contexto
  authenticated-data-source.js  RemoteGraphQLDataSource que reenvía headers de usuario/correlación
supergraph.yaml      Config de rover supergraph compose para los cuatro subgraphs
tests/
  product-entity.test.js  Pruebas de __resolveReference + batching con DataLoader (vitest)
```

## Uso

Instala las dependencias del subgraph:

```bash
npm install @apollo/server @apollo/subgraph graphql dataloader
npm install --save-dev vitest
```

Corre las pruebas:

```bash
npx vitest run tests/
```

Compone el supergraph en local (requiere [Rover](https://www.apollographql.com/docs/rover)):

```bash
rover supergraph compose --config supergraph.yaml > supergraph-schema.graphql
```

Los subgraphs `users` y `orders` en `supergraph.yaml` son placeholders:
reemplázalos por tus propios servicios o quita las entradas mientras experimentas.

## Notas

- `createDataSources`, `authenticateUser` y los objetos `db` referenciados en
  `server.js`/`resolvers.js` quedan deliberadamente a cargo de tu capa de datos;
  las pruebas muestran fakes mínimos para ellos.
- La versión de federación está fijada en `=2.0.0` en `supergraph.yaml`. Mantén
  alineada la versión de Rover en CI.
