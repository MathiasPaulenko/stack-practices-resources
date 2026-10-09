# Event Sourcing + CQRS in Python

Runnable implementation of an event-sourced bank account with CQRS separation,
based on the StackPractices recipe
[Implement Event Sourcing with CQRS in Python](https://stackpractices.com/recipes/event-sourcing-cqrs-pattern/).

## What's inside

| File | Contents |
| --- | --- |
| `events.py` | Pydantic domain events with per-instance `event_id`/`timestamp` factories and the event registry. |
| `aggregate.py` | `AggregateRoot` base + `BankAccount` with command methods that validate invariants and emit events. |
| `event_store.py` | Append-only event store on PostgreSQL with `UNIQUE(aggregate_id, version)` optimistic concurrency. |
| `handlers.py` | `CommandHandler`: load aggregate, run command, persist pending events. |
| `projectors.py` | `AccountProjector`, `AccountStatsProjector` and `ProjectorManager` with durable dedup (`processed_events`). |
| `queries.py` | `AccountQueryService` read side over projection tables. |
| `snapshots.py` | `SnapshotStore` + `load_aggregate` snapshot-and-replay helper. |
| `main.py` | End-to-end demo: commands → store → projections → queries → snapshot reload. |

## Run it

```bash
pip install -r requirements.txt
export DATABASE_URL=postgresql://user:pass@localhost/eventstore
python main.py
```

Tables are created automatically on first run (`event_store`, `snapshots`,
`processed_events`, `account_projection`, `transaction_projection`).

## Key design points

- `UNIQUE(aggregate_id, version)` is the real optimistic-concurrency guard; the
  `SELECT MAX(version)` check is only a fast path.
- Projection dedup lives in the `processed_events` table and commits in the same
  transaction as the projection update — idempotency survives restarts.
- `metadata` is a reserved attribute name in SQLAlchemy Declarative, so the model
  maps the column explicitly as `event_metadata`.
