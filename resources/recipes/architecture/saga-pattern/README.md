# Saga Pattern — Runnable Examples

Companion code for the [Saga Pattern recipe](https://stackpractices.com/recipes/saga-pattern-recipe/) on StackPractices.

## Files

- `orchestrator.ts` — TypeScript saga orchestrator with compensating transactions in reverse order, plus a Temporal/Cadence state-machine variant.
- `choreography_services.ts` — event-driven choreography: Order, Inventory and Payment services reacting to each other's events through an event bus.
- `OrderSagaManager.java` — Java Spring Boot orchestrator persisting saga state after every step and resuming interrupted compensations.
- `saga_state.sql` — PostgreSQL schema for saga instances (`saga_state`) and per-step audit (`saga_steps`).
- `saga_state_repository.py` — asyncpg repository to create, update and find stuck sagas.

## Notes

The TypeScript and Java files are illustrative: they assume `OrderService`, `InventoryService`, repositories and clients from your own codebase. The SQL schema runs as-is on PostgreSQL 14+.
