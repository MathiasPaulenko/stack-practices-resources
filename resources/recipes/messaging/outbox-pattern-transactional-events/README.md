# Transactional Outbox Pattern with Python

Reliable event publishing for microservices. The domain event is written to an `outbox_events` table inside the same database transaction as the business data; a separate relay drains unpublished rows to Kafka. You get at-least-once delivery without a distributed transaction coordinator.

## Files

| File | Contents |
| --- | --- |
| `schema.sql` | `outbox_events` table with status, retry and ordering indexes |
| `order_service.py` | `OrderService.create_order` — atomic business write + outbox insert in one transaction |
| `polling_relay.py` | `OutboxRelay` — scheduled polling with `FOR UPDATE SKIP LOCKED` and delivery callbacks |
| `transactional_relay.py` | `TransactionalOutboxRelay` — one Kafka transaction per batch to avoid partial publishes |
| `cdc_relay.py` | `CDCOutboxRelay` — PostgreSQL logical replication (wal2json) instead of polling |
| `ordered_relay.py` | `OrderedOutboxRelay` — per-aggregate ordering via Kafka key partitioning |
| `resilient_relay.py` | `ResilientOutboxRelay` — exponential backoff, retry limit, `FAILED` dead-letter status |
| `debezium-connector.yaml` | Debezium PostgresConnector + Outbox Event Router config |
| `multitenant-schema.sql` / `multitenant-relay.py` | `tenant_id` isolation variant |

## Usage

1. Apply `schema.sql` to your database.
2. Write events with the pattern in `order_service.py` — never publish to the broker inside the business transaction.
3. Run one relay: `polling_relay.py` to start, `cdc_relay.py` or the Debezium connector for low latency.
4. Keep consumers idempotent — the pattern guarantees at-least-once, not exactly-once.

Source: [Transactional Outbox recipe](https://stackpractices.com/recipes/outbox-pattern-transactional-events/)
