# Microservicios Event-Driven

Demos ejecutables de los tres patrones detrás de la receta de StackPractices
[Microservicios Event-Driven](https://stackpractices.com/es/recipes/event-driven-microservices/).
Sin dependencias externas — cada archivo corre por sí solo con stubs en memoria
donde en producción iría una base de datos o un broker.

## Contenido

| Archivo | Contenido |
| --- | --- |
| `event_sourcing.py` | Agregado de pedido + event store append-only con concurrencia optimista, más replay para reconstruir el estado. |
| `outbox.js` | Outbox transaccional: el pedido y la fila del outbox commitean en una transacción; un relay publica las pendientes en el broker (stub). |
| `order_saga.js` | Orquestación de saga con tres pasos y compensación; ejecuta el camino feliz y un fallo de pago para mostrar la cadena de rollback. |

## Ejecutar

```bash
python event_sourcing.py
node outbox.js
node order_saga.js
```

Python 3.10+ y Node 18+ (`await` de primer nivel en los demos JS). Para llevar
esto a producción, reemplaza los stubs en memoria por un store real
(PostgreSQL + knex/Prisma) y un productor real (kafkajs / kafka-python).
