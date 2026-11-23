# Patrón Outbox Transaccional con Python

Publicación confiable de eventos para microservicios. El evento de dominio se escribe en una tabla `outbox_events` dentro de la misma transacción que los datos de negocio; un relay separado vacía las filas no publicadas hacia Kafka. Obtienes entrega at-least-once sin un coordinador de transacciones distribuidas.

## Archivos

| Archivo | Contenido |
| --- | --- |
| `schema.sql` | Tabla `outbox_events` con índices de estado, reintentos y orden |
| `order_service.py` | `OrderService.create_order` — escritura de negocio + insert outbox atómicos en una transacción |
| `polling_relay.py` | `OutboxRelay` — polling programado con `FOR UPDATE SKIP LOCKED` y callbacks de entrega |
| `transactional_relay.py` | `TransactionalOutboxRelay` — una transacción de Kafka por lote para evitar publicaciones parciales |
| `cdc_relay.py` | `CDCOutboxRelay` — replicación lógica de PostgreSQL (wal2json) en lugar de polling |
| `ordered_relay.py` | `OrderedOutboxRelay` — orden por agregado mediante particionado por clave de Kafka |
| `resilient_relay.py` | `ResilientOutboxRelay` — backoff exponencial, límite de reintentos, estado `FAILED` dead-letter |
| `debezium-connector.yaml` | Config de PostgresConnector + Outbox Event Router de Debezium |
| `multitenant-schema.sql` / `multitenant-relay.py` | Variante con aislamiento por `tenant_id` |

## Uso

1. Aplica `schema.sql` a tu base de datos.
2. Escribe eventos con el patrón de `order_service.py` — nunca publiques al broker dentro de la transacción de negocio.
3. Ejecuta un relay: `polling_relay.py` para empezar, `cdc_relay.py` o el conector Debezium para baja latencia.
4. Mantén consumidores idempotentes — el patrón garantiza at-least-once, no exactly-once.

Fuente: [Receta Outbox Transaccional](https://stackpractices.com/es/recipes/outbox-pattern-transactional-events/)
