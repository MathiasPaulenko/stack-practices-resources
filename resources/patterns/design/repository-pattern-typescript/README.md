# Repository Pattern with TypeScript Generics — Companion Resource

Companion code for the StackPractices pattern [Repository Pattern with TypeScript Generics](https://stackpractices.com/patterns/repository-pattern-typescript/).

## Contents

- `repository.ts` — Generic `Repository<T, ID>` interface.
- `mongoose_repository.ts` — Mongoose-backed implementation with `toEntity` mapping.
- `in_memory_repository.ts` — In-memory implementation for fast unit tests.
- `user_service.ts` — Domain service that depends on the repository interface.
- `test_repository.ts` — Vitest tests covering CRUD, filtering, and service logic.
- `meta.json` — Resource metadata.

## Running the tests

```bash
npm install
npx vitest run
```

## Key concepts

- **Generic interface**: `Repository<T, ID>` works for any entity and id type.
- **Mongoose mapping**: `toEntity` strips `_id` and `__v`, returns plain entities.
- **In-memory for tests**: No database, no Docker, deterministic and fast.
- **Dependency injection**: `UserService` depends on the interface, not the concrete class.
