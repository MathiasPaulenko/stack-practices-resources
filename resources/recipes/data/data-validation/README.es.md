# Validación de Datos — Ejemplos Companion

Validadores de entrada de usuario ejecutables referenciados por la receta
[Validar y Sanitizar Datos de Entrada del Usuario](https://stackpractices.com/es/recipes/data-validation/).

## Archivos

| Archivo | Stack | Ejecutar |
|---------|-------|----------|
| `user_schema.ts` | Zod 4 (TypeScript) | `npx tsx user_schema.ts` |
| `user_model.py` | Pydantic v2 (Python) | `pip install "pydantic[email]" && python user_model.py` |
| `user_schema.js` | Joi 17 (Node.js) | `npm install joi && node user_schema.js` |

Los tres implementan el mismo esquema `User` —email, rango de edad, enum de
rol, lista de tags— para comparar sintaxis y salida de errores lado a lado.
