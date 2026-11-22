# Operaciones CRUD con MongoDB y Mongoose — Companion Offline

Companion ejecutable y sin dependencias de la receta de StackPractices
[Operaciones CRUD con MongoDB y Mongoose](https://stackpractices.com/es/recipes/mongodb-crud-mongoose/).

La receta usa Mongoose + un MongoDB real. Este companion reproduce la misma
semántica — validación, borrado suave con queries ocultas y rollback de
transacciones multi-escritura — contra un `DocumentStore` en memoria, para
estudiar y probar los patrones sin base de datos.

## Correr los tests

```bash
node --test user_store.test.mjs
```

## Qué cubre

- `create` / `find` / `findById` / `findByIdAndUpdate` — el ciclo CRUD completo.
- Validadores de campo con errores legibles, como los de Mongoose.
- `softDelete` — los docs borrados desaparecen de `find()` pero siguen
  consultables con `includeDeleted`.
- `withTransaction` — confirma todas las operaciones o revierte el batch
  completo ante un error.

## Relacionado

- Receta: https://stackpractices.com/es/recipes/mongodb-crud-mongoose/
- Inglés: https://stackpractices.com/recipes/mongodb-crud-mongoose/
