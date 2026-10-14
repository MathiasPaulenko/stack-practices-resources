# Patrón de Schema Stitching en GraphQL — Archivos complementarios

Ejemplo ejecutable de schema stitching para el patrón
[Patrón de Schema Stitching en GraphQL](https://stackpractices.com/es/patterns/graphql-schema-stitching-pattern/):
dos servicios GraphQL independientes fusionados tras un único gateway con
`@graphql-tools/stitch`.

## Archivos

| Archivo | Qué hace |
| --- | --- |
| `users-service.ts` | Subesquema `users-api` — tipo `User`, queries `user`/`users`, datos semilla. Sirve en :4001 de forma independiente. |
| `posts-service.ts` | Subesquema `posts-api` — tipo `Post` más la query en lote `postsByAuthorIds` que usa la variante de delegación en lote. Sirve en :4002. |
| `gateway.ts` | Construye los executors (`@graphql-tools/executor-http`), une ambos subesquemas, añade los tipos de enlace `extend type` y delega `User.posts` / `Post.author` vía `delegateToSchema`. Sirve en :4000. |
| `client-query.graphql` | La query de una-petición-dos-servicios de la página del patrón, con ejemplo `curl`. |
| `package.json` / `tsconfig.json` | Dependencias y configuración TypeScript estricta. |

## Ejecutar

```bash
npm install
npm run users    # users-api en :4001
npm run posts    # posts-api en :4002
npm run gateway  # esquema unido en :4000
```

Luego abre `client-query.graphql` y ejecútala contra `http://localhost:4000/graphql`.

## Notas

- `selectionSet` es obligatorio en los campos fusionados — `User.posts` necesita `{ id }` del usuario padre para construir la delegación `posts(authorId:)`.
- `mergeSchemas` y el paquete antiguo `schema-stitching` están deprecados; `stitchSchemas` de `@graphql-tools/stitch` es la API actual.
- `info` va tipado `any` en los resolvers de delegación por brevedad — los generics de `GraphQLResolveInfo` + `mergeInfo` también funcionan.
