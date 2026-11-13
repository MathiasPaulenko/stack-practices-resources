# Migración de GraphQL vs REST — Código complementario

Companion ejecutable de [GraphQL vs REST — Cuándo Elegir y Cómo Migrar](https://stackpractices.com/es/guides/graphql-vs-rest-guide/).

Demuestra los dos números más importantes de la guía con un contador de requests real:

- **Fase 1 (capa proxy)**: los resolvers ingenuos que llaman a endpoints REST se despliegan en 1 + N requests — una query de 10 posts cuesta **11 llamadas REST**.
- **Fase 2 (DataLoader)**: la misma query cuesta **2 llamadas REST** (lista de posts + un batch `/users?ids=`).
- **Fase 4 (persisted queries)**: hash `sha256` determinista de la query, mucho más corto que el texto.

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `rest-server.mjs` | API REST simulada (`/posts`, `/users`, `/users?ids=`, `/posts/:id/comments`) con contador global de requests |
| `api.mjs` | Cliente fetch mínimo para la API REST |
| `schema.mjs` | Schema GraphQL en SDL (`Post`, `User`, `Comment`, `Query`) |
| `resolvers.mjs` | `naiveResolvers` (N+1) y `batchedResolvers()` (DataLoader) |
| `server.mjs` | Instancia standalone de Apollo Server, conmutable entre naive/batched |
| `demo.mjs` | End-to-end: corre la misma query contra ambos resolver sets e imprime los conteos de requests REST |
| `tests/dataloader.test.js` | Vitest: conteos de requests, forma de respuesta (sin over-fetch), hashing de persisted queries |

## Ejecutar

```bash
npm install
npm run demo   # imprime naive 11 requests vs batched 2 requests
npm test       # 4 verificaciones vitest
```

Requiere Node 20+ (Apollo Server v5 y `fetch` global).
