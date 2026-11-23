# Outbox Pattern

Reliable event publishing for microservices: write the domain event to an `outbox` table in the same transaction as the business data, then let a separate relay forward unpublished rows to the broker. You get at-least-once delivery without a distributed transaction coordinator.

## Files

| File | Contents |
| --- | --- |
| `schema.sql` | Outbox table (id, aggregate, event_type, payload, published_at, retry_count) + partial index on unpublished rows |
| `outbox.py` | `DomainEvent`, `OutboxPublisher`, `OrderService`, and a polling `OutboxRelay` with `FOR UPDATE SKIP LOCKED` |
| `OutboxPublisher.java` | JDBC `OutboxPublisher` + `OrderService` with an atomic business write and outbox insert |
| `outbox.js` | `OutboxPublisher`, `OrderService`, and a polling `OutboxRelay` for Node/postgres |
| `retention-queries.sql` | Cleanup of published rows and an alerting query for stuck or retrying events |

## Usage

1. Run `schema.sql` to create the outbox table and its partial index.
2. In your service, call `publish()` on the outbox inside the same transaction as the business write.
3. Run the relay on a schedule (or switch to a CDC relay like Debezium for near real-time).
4. Schedule `retention-queries.sql` cleanup so the table does not grow forever.

Important: the pattern guarantees at-least-once delivery, not exactly-once. Consumers must be idempotent.

Source: [Outbox Pattern](https://stackpractices.com/patterns/outbox-pattern/)
