# Validación de Inputs en GraphQL — Schemas Zod en la frontera del resolver

Companion ejecutable de la receta de StackPractices
[Validación de Inputs en GraphQL con Zod](https://stackpractices.com/es/recipes/graphql-input-validation/).

## Qué incluye

- `src/schema.ts` — input types SDL (`CreatePostInput`, `UpdateUserInput`)
- `src/schemas.ts` — schemas Zod 4 más `validateInput`, que mapea los issues de `safeParse` a errores planos `{field, message}`
- `src/errors.ts` — `ValidationException` que transporta los errores por campo
- `src/resolvers.ts` — mutaciones que validan en la frontera antes de tocar la base de datos
- `src/server.ts` — `formatError` de Apollo Server 4 con `unwrapResolverError` (necesario: los errores de resolver llegan envueltos en `GraphQLError`)
- `src/demo.ts` — ejercita inputs válidos, inválidos y entre campos de punta a punta
- `tests/schemas.test.ts` — suite vitest que cubre transforms, forma del error, `path` entre campos y comportamiento del resolver

## Ejecutarlo

```bash
npm install
npm run demo    # node --experimental-strip-types src/demo.ts
npm test        # vitest run
```

Requiere Node.js ≥ 22.6 para `--experimental-strip-types`.

## Puntos clave

- Valida en la frontera del resolver, antes del acceso a base de datos.
- `safeParse` devuelve datos o un error tipado — nunca lanza.
- `.transform()` (trim, DOMPurify) produce salida saneada durante el parseo.
- Zod 4 movió los validadores ISO/formato al nivel superior: `z.iso.datetime()`, `z.email()`, `z.url()`.
- En Apollo Server 4, llama a `unwrapResolverError(error)` dentro de `formatError` antes de los `instanceof`.
