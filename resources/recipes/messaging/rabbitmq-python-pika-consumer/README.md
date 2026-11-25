# RabbitMQ Consumer with Python and Pika

Runnable companion code for the StackPractices recipe
[Build a RabbitMQ Consumer with Python and Pika](https://stackpractices.com/recipes/rabbitmq-python-pika-consumer/).

## Contents

- `producer.py` — publishes persistent JSON messages to a durable queue.
- `consumer.py` — consumer with manual acks, `prefetch_count=1` fair dispatch, and header-based retry before dead-lettering.
- `dlq_setup.py` — declares the dead-letter exchange (`dlx`), the DLQ, and the main queue with dead-letter arguments.
- `resilient_consumer.py` — consumer class that reconnects automatically on connection loss.

## Requirements

- Python 3.10+
- `pika` (`pip install pika`)
- RabbitMQ running locally (`docker run -p 5672:5672 rabbitmq:3`) or a remote host.

## Usage

```bash
# 1. Declare the queue with its DLX/DLQ
python dlq_setup.py

# 2. Start the consumer (or resilient consumer) in one terminal
python consumer.py task_queue
# python resilient_consumer.py

# 3. Publish a message in another terminal
python producer.py
```
