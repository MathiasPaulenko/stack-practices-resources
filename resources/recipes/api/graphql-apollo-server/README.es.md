# API GraphQL con Apollo Server — Companion

Proyecto runnable de Apollo Server + TypeScript que acompaña a la receta
[Construye una API GraphQL con Apollo Server y TypeScript](https://stackpractices.com/es/recipes/graphql-apollo-server/).

## Qué contiene

| Archivo | Propósito |
| --- | --- |
| `src/schema.ts` | TypeDefs schema-first con la directiva `@auth` |
| `src/resolvers.ts` | Resolvers de Query/Mutation/campos tipados contra el contexto |
| `src/context.ts` | Fábrica de contexto por petición: auth + DataLoader por request |
| `src/auth.ts` | Implementación de `@auth` mediante `mapSchema` |
| `src/db.ts` | Almacén en memoria de `users`/`posts` y un `verifyToken` de ejemplo |
| `src/server.ts` | Apollo Server standalone en el puerto 4000 |

## Ejecutarlo

```bash
npm install
npm run dev
```

Abre `http://localhost:4000/` y prueba:

```graphql
query {
  posts {
    title
    author { name }
  }
}
```

`Post.author` se resuelve a través del DataLoader por petición, así que
listar cincuenta posts sigue costando una sola consulta de usuarios.

## Mutación autenticada

Envía un token bearer `demo` (ver `verifyToken` en `src/db.ts`):

```graphql
mutation {
  createPost(title: "Nuevo post", content: "Cuerpo") {
    id
    author { name }
  }
}
```

```bash
curl -X POST http://localhost:4000/ \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer demo' \
  -d '{"query":"mutation { createPost(title: \"Nuevo post\", content: \"Cuerpo\") { id } }"}'
```

Sin la cabecera, la directiva `@auth` devuelve `Unauthorized`.

## Notas

- `verifyToken` es un stub: `"demo"` mapea al usuario semilla `u1`.
  Sustitúyelo por tu verificación real (JWT, sesiones).
- `db` está en memoria; cámbialo por tu ORM o driver. Las firmas de los
  resolvers no cambian.
