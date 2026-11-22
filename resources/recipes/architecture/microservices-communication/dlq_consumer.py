"""Async message consumer with retry-via-requeue and a dead-letter queue.

Companion to https://stackpractices.com/recipes/microservices-communication/
Requires: pika (see requirements.txt) and RabbitMQ reachable at RABBITMQ_URL
(default amqp://rabbitmq:5672).

Failed messages are republished with an incremented `x-retry-count` header;
after 3 attempts they land in `orders.created.dlq` for manual inspection.
"""

import json
import logging
import os

import pika

logger = logging.getLogger(__name__)


class OrderConsumer:
    def __init__(self, rabbitmq_url: str = "amqp://rabbitmq:5672"):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(rabbitmq_url)
        )
        self.channel = self.connection.channel()

        # Main queue
        self.channel.queue_declare(queue="orders.created", durable=True)
        # Dead-letter queue for failed messages
        self.channel.queue_declare(queue="orders.created.dlq", durable=True)

    def process_message(self, ch, method, properties, body):
        try:
            order = json.loads(body)
            self._handle_order(order)
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            logger.error(f"Failed to process order: {e}")
            # Reject and requeue up to 3 times, then send to DLQ
            headers = properties.headers or {}
            retry_count = headers.get("x-retry-count", 0)
            if retry_count < 3:
                ch.basic_publish(
                    exchange="",
                    routing_key="orders.created",
                    body=body,
                    properties=pika.BasicProperties(
                        headers={"x-retry-count": retry_count + 1}
                    ),
                )
            else:
                ch.basic_publish(
                    exchange="",
                    routing_key="orders.created.dlq",
                    body=body,
                    properties=pika.BasicProperties(
                        headers={"x-retry-count": retry_count + 1}
                    ),
                )
            ch.basic_ack(delivery_tag=method.delivery_tag)

    def _handle_order(self, order: dict):
        logger.info(f'Processing order {order["id"]}')
        # Business logic here

    def start(self):
        self.channel.basic_consume(
            queue="orders.created",
            on_message_callback=self.process_message,
        )
        logger.info("Waiting for orders...")
        self.channel.start_consuming()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    OrderConsumer(os.environ.get("RABBITMQ_URL", "amqp://rabbitmq:5672")).start()
