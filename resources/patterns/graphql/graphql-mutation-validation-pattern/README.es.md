# GraphQL Mutation Validation: Validación Centralizada

Código companion para el [patrón GraphQL Mutation Validation](https://stackpractices.com/es/patterns/graphql-mutation-validation-pattern/) en StackPractices.

## Archivos

| Archivo | Descripción |
| --- | --- |
| `validation.ts` | Framework de validación: `validateInput` y `collectErrors` |
| `rules.ts` | Factorías de reglas de validación reutilizables (required, minLength, email, range, url) |
| `scalars.ts` | Helpers del scalar Email personalizado (sin dependencias) |
| `test_validation.ts` | Tests unitarios para todos los módulos (15 tests) |

## Setup

```bash
npm install -g ts-node typescript
```

## Ejecutar los tests

```bash
npx ts-node test_validation.ts
```

## Uso

```typescript
import { validateInput } from "./validation";
import { rules } from "./rules";

validateInput(input, [
  rules.required("name"),
  rules.minLength("name", 2),
  rules.email("email"),
]);
// lanza si la validación falla, pasa silenciosamente si es válido
```

## Uso en producción

En producción con el paquete `graphql` instalado, reemplazá el `Error` plain
en `validation.ts` con un `GraphQLError`:

```typescript
import { GraphQLError } from "graphql";

throw new GraphQLError("Validation failed", {
  extensions: {
    code: "VALIDATION_ERROR",
    fields: errors.map(e => e.field),
    errors,
    timestamp: new Date().toISOString(),
  },
});
```
