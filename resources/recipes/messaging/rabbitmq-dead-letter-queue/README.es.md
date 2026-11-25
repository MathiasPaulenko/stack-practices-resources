# Dead-Letter Queues en RabbitMQ — Recursos complementarios

Código ejecutable de la receta
[Dead-Letter Queues en RabbitMQ para Mensajes Fallidos](https://stackpractices.com/es/recipes/rabbitmq-dead-letter-queue/).

| Archivo | Propósito |
| --- | --- |
| `dlq_setup.py` | Declara una cola con su DLX + DLQ, expiración TTL, overflow por max-length y colas de retry con TTL |
| `consumer_with_retry.py` | Consumer que dead-letter errores de validación y reintenta los transitorios a través de las colas de retry |
| `dlq_tools.py` | CLI para inspeccionar mensajes de la DLQ, leer las razones de `x-death` y replayar mensajes a la cola principal |

## Inicio rápido

```bash
pip install pika          # RabbitMQ corriendo en localhost:5672
python dlq_setup.py       # declara orders, orders.dlq y las colas de retry
python consumer_with_retry.py orders
python dlq_tools.py inspect orders.dlq
python dlq_tools.py replay orders.dlq orders
```

Los argumentos de cola son inmutables — si una cola ya existe sin los
argumentos `x-dead-letter-*`, bórrala y redeclárala, o aplica una
operator policy en su lugar.
