# Receta CQRS — Recursos complementarios

Ejemplos de código de la receta [Escalar Cargas de Lectura y Escritura con CQRS](https://stackpractices.com/es/recipes/cqrs-pattern-recipe/).

## Archivos

| Archivo | Qué muestra |
|---------|-------------|
| `command-handler.ts` | Manejador de comandos con publicación de eventos: `Event`, `EventStore`, `OrderWriteModel` y `PayOrderHandler` con rehidratación por eventos (TypeScript) |
| `order-projection.sql` | Modelo de lectura desnormalizado `order_summaries` con proyección basada en trigger (PostgreSQL) |
| `order-projection.js` | Manejador de eventos que actualiza un modelo de lectura relacional y un índice de Elasticsearch (Node.js) |
| `event-sourcing.py` | Lado de escritura completo con `EventStore` abstracto, manejador de comandos y rehidratación por replay (Python) |
| `snapshotting.ts` | `SnapshotStore` y un manejador de comandos que carga el snapshot y solo reproduce los eventos posteriores (TypeScript) |
| `redis-read-model.ts` | Modelo de lectura sobre hashes de Redis con manejadores `hgetall`/`hset` (TypeScript) |

## Notas

- Son snippets didácticos, no un proyecto ejecutable — conéctalos a tu propia implementación de `EventStore` (EventStoreDB, PostgreSQL, Kafka, etc.).
- Las proyecciones deben ser idempotentes: un manejador puede recibir el mismo evento más de una vez.
