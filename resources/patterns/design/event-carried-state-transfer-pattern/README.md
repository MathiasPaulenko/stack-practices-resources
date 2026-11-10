# Event-Carried State Transfer Pattern — Runnable Implementations

Companion to the StackPractices pattern [Event-Carried State Transfer Pattern](https://stackpractices.com/patterns/event-carried-state-transfer-pattern/).

An ECST demo in three equivalent implementations: a `CustomerService` that owns customer data, an in-memory event bus standing in for Kafka, and an `OrderService` consumer that applies each state-transfer event to a local replica and serves reads without calling the source. Every event carries the full entity state plus a `version` sequence number, so consumers can spot out-of-order or duplicate deliveries. Stdlib only — no dependencies needed.

## Files

| File | Stack | Run |
| --- | --- | --- |
| `src/ecst.py` | Python 3.9+ (stdlib only) | `python src/ecst.py` |
| `src/ecst.js` | Node.js 14+ (stdlib only) | `node src/ecst.js` |
| `src/EventCarriedStateTransfer.java` | Java 16+ (`record`, `var`) | `javac src/EventCarriedStateTransfer.java && java -cp src EventCarriedStateTransfer` |

Each run prints the replication log: the customer creation event, the local read served from the replica, the tier-update event and the updated local copy. In production you'd swap the in-memory `EventBus` for a Kafka topic (the article shows the Spring Cloud Stream variant) and the replica `Map`/SQLite table for whichever store the consumer already uses — the apply-and-read logic stays identical.
