# Dead Letter Queues — Companion Resources

Runnable code referenced by
[Dead Letter Queues: Setup for SQS, RabbitMQ & Kafka](https://stackpractices.com/recipes/dead-letter-queue/).

| File | Purpose |
| --- | --- |
| `sqs-dlq-setup.sh` | AWS CLI: create queue + DLQ and attach the redrive policy (`maxReceiveCount=3`) |
| `rabbitmq_dlq_consumer.py` | pika consumer with DLX declaration and `basic_reject(requeue=False)` routing |
| `kafka_dlq_consumer.js` | KafkaJS consumer that publishes failed messages to `orders-dlq` with error headers |

Each broker dead-letters differently: SQS at the broker (redrive policy),
RabbitMQ through a dead-letter exchange, Kafka entirely in client code.
Stamp every DLQ message with error type, origin, and retry count — without
that context, replay is guesswork.
