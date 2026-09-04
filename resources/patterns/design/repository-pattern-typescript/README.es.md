# Repository Pattern con Generics de TypeScript — Recurso Companion

Código companion del patrón de StackPractices [Repository Pattern con Generics de TypeScript](https://stackpractices.com/es/patterns/repository-pattern-typescript/).

## Contenidos

- `repository.ts` — Interfaz genérica `Repository<T, ID>`.
- `mongoose_repository.ts` — Implementación con Mongoose y mapeo `toEntity`.
- `in_memory_repository.ts` — Implementación en memoria para tests unitarios rápidos.
- `user_service.ts` — Servicio de dominio que depende de la interfaz del repositorio.
- `test_repository.ts` — Tests con Vitest cubriendo CRUD, filtrado y lógica del servicio.
- `meta.json` — Metadata del recurso.

## Ejecutar los tests

```bash
npm install
npx vitest run
```

## Conceptos clave

- **Interfaz genérica**: `Repository<T, ID>` funciona para cualquier entidad y tipo de id.
- **Mapeo Mongoose**: `toEntity` elimina `_id` y `__v`, devuelve entidades planas.
- **En memoria para tests**: Sin base de datos, sin Docker, determinístico y rápido.
- **Inyección de dependencias**: `UserService` depende de la interfaz, no de la clase concreta.
