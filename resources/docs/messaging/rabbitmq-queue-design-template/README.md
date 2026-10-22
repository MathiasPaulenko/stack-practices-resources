# RabbitMQ Queue Design Template — Companion

Companion project for the [RabbitMQ Queue Design Template](https://stackpractices.com/docs/rabbitmq-queue-design-template/). A minimal but complete pika setup that declares the template's topology and exercises the retry → DLX flow.

## Files

| File | What it does |
|------|--------------|
| `declare_topology.py` | Declares exchange, queue (with DLX + TTL + max-length), dead-letter queue, and all bindings |
| `producer.py` | Publishes persistent messages with `confirm_delivery` and `mandatory=True` |
| `consumer.py` | Manual ack + republish-based retry counter (correct version — plain `basic_reject(requeue=True)` cannot increment headers) |

## Usage

```bash
pip install pika
export RABBITMQ_USER=guest RABBITMQ_PASSWORD=guest RABBITMQ_HOST=localhost

python declare_topology.py   # idempotent — safe to re-run
python producer.py           # publishes 5 orders
python consumer.py           # processes with retries + DLX fallback
```

Watch the flow in the RabbitMQ management UI (`http://localhost:15672`): messages move from the main queue to `prod.orders.dlq.failed-messages` after 3 retries.

Note: `properties.headers` can be `None` on messages published without headers — always read it with `dict(properties.headers or {})`.
