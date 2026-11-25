# Saga Pattern — Ejemplos ejecutables

Código companion de la [receta del Saga Pattern](https://stackpractices.com/es/recipes/saga-pattern-recipe/) en StackPractices.

## Archivos

- `orchestrator.ts` — TypeScript saga orchestrator with compensating transactions in reverse order, plus a Temporal/Cadence state-machine variant.
- `choreography_services.ts` — event-driven choreography: Order, Inventory and Payment services reacting to each other's events through an event bus.
- `OrderSagaManager.java` — Java Spring Boot orchestrator persisting saga state after every step and resuming interrupted compensations.
- `saga_state.sql` — PostgreSQL schema for saga instances (`saga_state`) and per-step audit (`saga_steps`).
- `saga_state_repository.py` — asyncpg repository to create, update and find stuck sagas.

## Notas

Los archivos TypeScript y Java son ilustrativos: asumen `OrderService`, `InventoryService`, repositorios y clientes de tu propio código. El esquema SQL corre tal cual en PostgreSQL 14+.
