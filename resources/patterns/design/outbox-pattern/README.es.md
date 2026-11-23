# Patrón Outbox

Publicación confiable de eventos para microservicios: escribe el evento de dominio en una tabla `outbox` dentro de la misma transacción que los datos de negocio, y deja que un relay separado reenvíe las filas no publicadas al broker. Obtienes entrega at-least-once sin un coordinador de transacciones distribuidas.

## Archivos

| Archivo | Contenido |
| --- | --- |
| `schema.sql` | Tabla outbox (id, aggregate, event_type, payload, published_at, retry_count) + índice parcial sobre filas no publicadas |
| `outbox.py` | `DomainEvent`, `OutboxPublisher`, `OrderService` y un `OutboxRelay` de polling con `FOR UPDATE SKIP LOCKED` |
| `OutboxPublisher.java` | `OutboxPublisher` JDBC + `OrderService` con escritura de negocio e insert en outbox atómicos |
| `outbox.js` | `OutboxPublisher`, `OrderService` y un `OutboxRelay` de polling para Node/postgres |
| `retention-queries.sql` | Limpieza de filas publicadas y consulta de alerta para eventos atascados o reintentando |

## Uso

1. Ejecuta `schema.sql` para crear la tabla outbox y su índice parcial.
2. En tu servicio, llama a `publish()` del outbox dentro de la misma transacción que la escritura de negocio.
3. Corre el relay de forma programada (o cambia a un relay CDC como Debezium para casi tiempo real).
4. Programa la limpieza de `retention-queries.sql` para que la tabla no crezca indefinidamente.

Importante: el patrón garantiza entrega at-least-once, no exactly-once. Los consumidores deben ser idempotentes.

Fuente: [Patrón Outbox](https://stackpractices.com/es/patterns/outbox-pattern/)
