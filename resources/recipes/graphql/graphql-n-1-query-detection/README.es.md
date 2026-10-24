# Detección de consultas N+1 en GraphQL — Detector ejecutable

Versión ejecutable de la receta de StackPractices
[Detectar y corregir consultas N+1 en resolvers GraphQL](https://stackpractices.com/es/recipes/graphql-n-1-query-detection/).

Proyecto con Apollo Server 4 que cuenta las consultas a la base de datos por
petición mediante un cliente instrumentado, alerta de sospechas de N+1 dentro
de `willSendResponse` y corrige el patrón con batching de DataLoader por
petición sobre un store en memoria.

## Archivos

| Archivo | Propósito |
| --- | --- |
| `src/instrumented.ts` | Wrapper con proxy que registra cada llamada a la BD en un `QueryLog`. |
| `src/queryLogger.ts` | Plugin de Apollo que lee el conteo desde `contextValue` en `willSendResponse`. |
| `src/loaders.ts` | `createUserLoader` — DataLoader por petición para autores. |
| `src/resolvers.ts` | Esquema + resolvers, con el resolver N+1 ingenuo comentado. |
| `src/server.ts` | Conecta `QueryLog`, cliente instrumentado y loaders nuevos por petición. |

## Uso

```bash
npm install
npm start
```

Abre `http://localhost:4000` y ejecuta:

```graphql
query {
  posts {
    id
    title
    author {
      name
    }
  }
}
```

Con el resolver batched, la operación emite 2 consultas. Cambia al resolver
ingenuo comentado en `src/resolvers.ts` para ver el warning `[N+1 SUSPECT]`
reportar 21 consultas.
