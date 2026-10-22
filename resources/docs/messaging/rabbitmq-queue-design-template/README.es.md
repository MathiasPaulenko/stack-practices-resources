# Plantilla de Diseño de Colas RabbitMQ — Companion

Proyecto complementario de la [Plantilla de Diseño de Colas RabbitMQ](https://stackpractices.com/es/docs/rabbitmq-queue-design-template/). Un setup de pika mínimo pero completo que declara la topología de la plantilla y ejercita el flujo de reintentos → DLX.

## Archivos

| Archivo | Qué hace |
|---------|----------|
| `declare_topology.py` | Declara exchange, cola (con DLX + TTL + max-length), dead-letter queue y todos los bindings |
| `producer.py` | Publica mensajes persistentes con `confirm_delivery` y `mandatory=True` |
| `consumer.py` | Ack manual + contador de reintentos por republicación (versión correcta — `basic_reject(requeue=True)` no puede incrementar cabeceras) |

## Uso

```bash
pip install pika
export RABBITMQ_USER=guest RABBITMQ_PASSWORD=guest RABBITMQ_HOST=localhost

python declare_topology.py   # idempotente — se puede reejecutar
python producer.py           # publica 5 pedidos
python consumer.py           # procesa con reintentos + fallback al DLX
```

Observa el flujo en la UI de administración de RabbitMQ (`http://localhost:15672`): los mensajes pasan de la cola principal a `prod.orders.dlq.failed-messages` tras 3 reintentos.

Nota: `properties.headers` puede ser `None` en mensajes publicados sin cabeceras — léelo siempre con `dict(properties.headers or {})`.
