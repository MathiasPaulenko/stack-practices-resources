# Checklist de Revisión de Esquemas GraphQL — Código complementario

Companion ejecutable del [Checklist de Revisión de Esquemas GraphQL](https://stackpractices.com/es/docs/graphql-schema-review-checklist/).

Automatiza el subconjunto de ítems del checklist que un parser puede verificar, para conectarlo en CI y reservar la revisión humana para las decisiones de criterio (nulabilidad, contrato de errores, configuración de seguridad).

## Qué incluye

- `review.mjs` — checker de SDL construido sobre `graphql.parse`. Comprueba:
  - Nombres de tipos en PascalCase
  - Nombres de campos en camelCase
  - Campos `Boolean` que empiezan por `is`/`has`/`can`
  - Campos `id` tipados como `ID`
  - Campos de lista en Query con argumentos de paginación por cursor, y sin `offset`
  - Mutaciones con nombre de verbo, un único argumento `input` y retorno `*Payload`
  - Payload types que exponen `userErrors`
  - Valores de enum en UPPER_SNAKE_CASE
  - `@deprecated` siempre con `reason`
- `schemas/good-schema.graphqls` — un esquema que pasa todos los checks
- `schemas/bad-schema.graphqls` — un esquema que falla a propósito, una violación por ítem del checklist
- `demo.mjs` — imprime el informe de revisión de ambos esquemas
- `tests/review.test.js` — verifica que el esquema bueno pasa y el malo falla en cada check

## Cómo ejecutarlo

```bash
npm install
npm run demo    # informe de ambos esquemas
npm test        # vitest
node review.mjs ruta/a/tu/schema.graphqls   # revisa tu propio esquema
```

El código de salida es distinto de cero cuando falla algún check, así que entra directo en un job de CI.

## Qué NO comprueba

Límites de profundidad/complejidad, N+1, política de introspección y composición de federación: viven en la configuración del servidor o necesitan `graphql-inspector`/`rover`, como explican las notas de "Cómo verificar" del documento.
