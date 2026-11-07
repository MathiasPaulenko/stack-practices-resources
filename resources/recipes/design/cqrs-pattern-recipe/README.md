# CQRS Recipe — Companion Resources

Code examples from the recipe [Scale Read and Write Workloads with CQRS](https://stackpractices.com/recipes/cqrs-pattern-recipe/).

## Files

| File | What it shows |
|------|---------------|
| `command-handler.ts` | Command handler with event publishing: `Event`, `EventStore`, `OrderWriteModel`, and `PayOrderHandler` with event rehydration (TypeScript) |
| `order-projection.sql` | Denormalized read model `order_summaries` plus a trigger-based projection handler (PostgreSQL) |
| `order-projection.js` | Event handler updating a relational read model and an Elasticsearch index (Node.js) |
| `event-sourcing.py` | Full write side with an abstract `EventStore`, command handler and replay-based rehydration (Python) |
| `snapshotting.ts` | `SnapshotStore` and a command handler that loads a snapshot and only replays events after it (TypeScript) |
| `redis-read-model.ts` | Read model backed by Redis hashes with `hgetall`/`hset` projection handlers (TypeScript) |

## Notes

- These are teaching snippets, not a runnable project — wire them to your own `EventStore` implementation (EventStoreDB, PostgreSQL, Kafka, etc.).
- Projections must be idempotent: handlers can receive the same event more than once.
