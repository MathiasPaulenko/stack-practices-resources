# Validación de Datos con Zod — Ejemplos Companion

Ejemplos ejecutables de la receta [Validación de datos con esquemas de Zod en TypeScript](https://stackpractices.com/es/recipes/data-validation-zod/). Todos los esquemas usan la API de primer nivel de **Zod 4** (`z.uuid()`, `z.email()`, `z.url()`).

## Archivos

| Archivo | Qué muestra |
|---------|-------------|
| `schemas/user.ts` | Esquema de objeto básico, `z.infer`, reglas `.refine` para contraseñas |
| `schemas/env.ts` | Validación fail-fast de `process.env` al arrancar con `z.coerce` |
| `schemas/webhook.ts` | `z.discriminatedUnion` para payloads de webhook polimórficos |
| `middleware/validate-body.ts` | Middleware de Express + `error.issues` → `{ campo: mensaje }` |

## Ejecutar

```bash
npm install zod
node --experimental-strip-types schemas/user.ts
```

`env.ts` y `webhook.ts` están pensados para integrarse en un proyecto — `env.ts` termina el proceso si la configuración es inválida, y `validate-body.ts` necesita los tipos de `express`.
