# RabbitMQ Dead-Letter Queues — Companion Resources

Runnable code referenced by
[Configure Dead-Letter Queues in RabbitMQ for Failed Messages](https://stackpractices.com/recipes/rabbitmq-dead-letter-queue/).

| File | Purpose |
| --- | --- |
| `dlq_setup.py` | Declare a queue with its DLX + DLQ, TTL expiry, max-length overflow, and TTL retry queues |
| `consumer_with_retry.py` | Consumer that dead-letters validation errors and retries transient ones through the retry queues |
| `dlq_tools.py` | CLI to inspect DLQ messages, read `x-death` reasons, and replay messages to the main queue |

## Quick start

```bash
pip install pika          # RabbitMQ running on localhost:5672
python dlq_setup.py       # declares orders, orders.dlq and retry queues
python consumer_with_retry.py orders
python dlq_tools.py inspect orders.dlq
python dlq_tools.py replay orders.dlq orders
```

Queue arguments are immutable — if a queue already exists without the
`x-dead-letter-*` arguments, delete and redeclare it, or apply an operator
policy instead.
