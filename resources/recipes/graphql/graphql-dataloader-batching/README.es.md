# GraphQL DataLoader Batching — Companion

Companion ejecutable de la receta de StackPractices
[Agrupa y cachea consultas a la BD con DataLoader en GraphQL](https://stackpractices.com/es/recipes/graphql-dataloader-batching/).

## Qué contiene

- `src/mock-db.ts` — tablas `users`/`posts` en memoria que cuentan cada consulta simulada a la base de datos.
- `src/loaders.ts` — `createUserLoader` (loader de entidad) y `createPostsByAuthorLoader` (loader uno-a-muchos). Ambos devuelven arrays de resultados alineados con las claves de entrada.
- `src/context.ts` — fábrica de contexto por petición; un DataLoader nuevo por petición mantiene la caché aislada.
- `src/demo.ts` — demo ejecutable que muestra el conteo de consultas N+1 frente a lotes, deduplicación de caché, alineación de `loadMany`, errores por clave, invalidación tras mutación con `clear()` y el loader uno-a-muchos.

## Ejecutarlo

```bash
npm install
npm start        # tsx src/demo.ts
npm run typecheck
```

Salida esperada: los resolvers ingenuos emiten 6 consultas para 5 posts; DataLoader emite 2. Tres llamadas `load('u1')` tocan la base de datos una sola vez. `loadMany(['u1','missing'])` devuelve `Ada` más un `Error` por clave. Una mutación seguida de `clear('u1')` refresca la entidad cacheada.
