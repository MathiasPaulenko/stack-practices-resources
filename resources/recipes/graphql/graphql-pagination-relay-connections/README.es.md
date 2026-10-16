# Paginación por cursores Relay en GraphQL — Companion

Companion ejecutable de la [receta Relay Connections](https://stackpractices.com/es/recipes/graphql-pagination-relay-connections/) en StackPractices.

## Contenido

| Archivo | Qué es |
|---------|--------|
| `src/schema.ts` | Definiciones de tipos `PageInfo` / `PostEdge` / `PostConnection` / `PaginationInput` |
| `src/cursor.ts` | `encodeCursor` / `decodeCursor` (base64) |
| `src/resolvers.ts` | Resolver bidireccional: `first`/`after` hacia adelante, `last`/`before` hacia atrás, truco `take + 1` |
| `src/server.ts` | Apollo Server con store en memoria (57 posts sembrados) |
| `package.json` | dependencias + `npm start` |

## Ejecútalo

```bash
npm install
npm start
```

Abre la URL impresa y prueba:

```graphql
query {
  posts(pagination: { first: 5 }) {
    edges { cursor node { id title } }
    pageInfo { hasNextPage endCursor }
  }
}
```

Toma el `endCursor` y pásalo como `after` para la página siguiente.

Receta fuente: https://stackpractices.com/es/recipes/graphql-pagination-relay-connections/
