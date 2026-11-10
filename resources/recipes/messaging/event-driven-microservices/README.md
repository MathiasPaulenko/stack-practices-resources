# Event-Driven Microservices

Runnable demos of the three patterns behind the StackPractices recipe
[Event-Driven Microservices](https://stackpractices.com/recipes/event-driven-microservices/).
No external dependencies — every file runs standalone with in-memory stubs
where a database or broker would sit in production.

## What's inside

| File | Contents |
| --- | --- |
| `event_sourcing.py` | Order aggregate + append-only event store with optimistic concurrency, plus replay to rebuild state. |
| `outbox.js` | Transactional outbox: order and outbox row commit in one transaction; a relay publishes pending rows to the (stubbed) broker. |
| `order_saga.js` | Saga orchestration with three steps and compensation; runs the happy path and a payment failure to show the rollback chain. |

## Run it

```bash
python event_sourcing.py
node outbox.js
node order_saga.js
```

Python 3.10+ and Node 18+ (top-level `await` in the JS demos). To move these
to production, replace the in-memory stubs with a real store
(PostgreSQL + knex/Prisma) and a real producer (kafkajs / kafka-python).
