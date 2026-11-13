# Tipos escalares GraphQL personalizados — Implementaciones ejecutables

Versión ejecutable de la receta de StackPractices
[Escalares GraphQL personalizados: fechas, emails y JSON](https://stackpractices.com/es/recipes/graphql-custom-scalar-types/).

Cinco implementaciones de `GraphQLScalarType` que cubren las tres direcciones
que un escalar debe manejar — `serialize` (servidor → cliente), `parseValue`
(variable GraphQL → servidor) y `parseLiteral` (nodo AST inline → servidor) —
más un script demo que ejercita cada una.

## Archivos

| Archivo | Propósito |
| --- | --- |
| `src/scalars/Date.ts` | Escalar de fecha ISO 8601 con `specifiedByURL` apuntando a RFC 3339. |
| `src/scalars/Email.ts` | Escalar de email que valida formato y normaliza a minúsculas. |
| `src/scalars/JSON.ts` | Escalar JSON passthrough que recorre recursivamente los nodos AST `List`/`Object`. |
| `src/scalars/URL.ts` | Escalar de URL que exige `http:`/`https:` mediante el parser WHATWG `URL`. |
| `src/scalars/PositiveInt.ts` | Escalar de dominio que rechaza cero, negativos y no enteros. |
| `src/schema.ts` | SDL + mapa de resolvers que muestra cómo se registran los escalares. |
| `src/demo.ts` | Ejecuta entradas válidas e inválidas por las tres funciones e imprime resultados. |

## Uso

```bash
npm install
npm start        # ejecuta la demo con tsx
npm run typecheck
```

Para conectar los escalares a un servidor real, copia la carpeta `scalars/` y
fusiona las entradas del mapa `resolvers` de `src/schema.ts` en tu configuración
de Apollo Server o `makeExecutableSchema`.
