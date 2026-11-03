# Patrón CDC — Debezium, Kafka y Ejemplos de Consumidor

Código companion del [patrón CDC (Change Data Capture)](https://stackpractices.com/es/patterns/cdc-change-data-capture-pattern/) de StackPractices.

## Archivos

- `docker-compose.yml` — stack con PostgreSQL (WAL lógico), Kafka + Zookeeper y Debezium Connect. Ejecuta con `docker compose up -d`.
- `register-postgres-connector.json` — configuración del conector Debezium (pgoutput, modo snapshot, transformación unwrap). Regístralo con `curl -X POST -H "Content-Type: application/json" -d @register-postgres-connector.json http://localhost:8083/connectors`.
- `src/cdc_consumer.py` — consumidor Python que transmite eventos CDC de Kafka a Elasticsearch, confirmando offsets solo tras procesar con éxito.
- `src/outbox_relay.py` — relay de outbox transaccional: lee las filas sin procesar de la tabla `outbox` (`FOR UPDATE SKIP LOCKED`) y las publica en topics de Kafka.
- `src/reconciliation.py` — verificador periódico que compara conteos del origen con el índice destino y re-sincroniza registros perdidos.

## Requisitos

- Docker + docker compose para el stack
- Python 3.9+ con `kafka-python`, `elasticsearch`, `psycopg2-binary` para los scripts consumidores
