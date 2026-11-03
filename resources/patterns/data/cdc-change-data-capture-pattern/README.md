# CDC Pattern — Debezium, Kafka and Consumer Examples

Companion code for the [CDC (Change Data Capture) pattern](https://stackpractices.com/patterns/cdc-change-data-capture-pattern/) on StackPractices.

## Files

- `docker-compose.yml` — PostgreSQL (logical WAL), Kafka + Zookeeper, and Debezium Connect stack. Run with `docker compose up -d`.
- `register-postgres-connector.json` — Debezium connector config (pgoutput, snapshot mode, unwrap transform). Register with `curl -X POST -H "Content-Type: application/json" -d @register-postgres-connector.json http://localhost:8083/connectors`.
- `src/cdc_consumer.py` — Python consumer that streams CDC events from Kafka into Elasticsearch, committing offsets only after successful processing.
- `src/outbox_relay.py` — transactional outbox relay: reads unprocessed rows from the `outbox` table (`FOR UPDATE SKIP LOCKED`) and publishes them to Kafka topics.
- `src/reconciliation.py` — periodic checker that compares source counts with the target index and re-syncs missing records.

## Requirements

- Docker + docker compose for the stack
- Python 3.9+ with `kafka-python`, `elasticsearch`, `psycopg2-binary` for the consumer scripts
