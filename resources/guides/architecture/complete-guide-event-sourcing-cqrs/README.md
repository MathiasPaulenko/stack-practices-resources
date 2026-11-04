# Event Sourcing and CQRS — Companion Assets

Runnable pieces from
[Event Sourcing and CQRS: Event Store, Projections](https://stackpractices.com/guides/complete-guide-event-sourcing-cqrs/).

## Contents

| File | What it shows |
| --- | --- |
| `event-store-schema.sql` | `events` + `snapshots` tables with `UNIQUE(stream_id, version)` |
| `EventStore.ts` | Append-only store with optimistic concurrency |
| `OrderAggregate.ts` | Aggregate root: `raise`/`apply`/`loadFromHistory` |
| `OrderProjection.ts` | Read model builder subscribed to events |
| `SnapshotStore.ts` | Snapshot save/load to skip long replays |

## Usage

The files are the reference implementation — compose them in your app or adapt to EventStoreDB/Axon for higher throughput.
