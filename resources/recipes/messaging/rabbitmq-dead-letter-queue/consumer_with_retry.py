"""Consumer that retries transient failures through TTL retry queues
and dead-letters messages that exhaust retries or fail validation.

Usage:
    python consumer_with_retry.py orders
"""

import json
import sys

import pika

MAX_RETRIES = 4


class ValidationError(Exception):
    pass


class TransientError(Exception):
    pass


def process_message(message: dict) -> None:
    if "id" not in message:
        raise ValidationError("missing id")
    # real work here


def send_to_retry(channel, base_queue: str, body: bytes, attempt: int) -> None:
    channel.basic_publish(
        exchange="",
        routing_key=f"{base_queue}.retry.{attempt}",
        body=body,
        properties=pika.BasicProperties(
            delivery_mode=2,
            headers={"x-retry-attempt": attempt + 1},
            content_type="application/json",
        ),
    )


def consume_with_backoff(channel, base_queue: str, max_retries: int = MAX_RETRIES):
    def callback(ch, method, properties, body):
        message = json.loads(body)
        attempt = (properties.headers or {}).get("x-retry-attempt", 0)

        try:
            process_message(message)
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except ValidationError as e:
            print(f"Validation error, dead-lettering: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        except Exception as e:
            if attempt < max_retries:
                send_to_retry(ch, base_queue, body, attempt)
                ch.basic_ack(delivery_tag=method.delivery_tag)
            else:
                ch.basic_publish(
                    exchange="",
                    routing_key=f"{base_queue}.dlq",
                    body=body,
                    properties=pika.BasicProperties(
                        delivery_mode=2,
                        headers={"x-retry-attempt": attempt, "x-final-error": str(e)},
                        content_type="application/json",
                    ),
                )
                ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue=base_queue, on_message_callback=callback)
    channel.start_consuming()


if __name__ == "__main__":
    queue = sys.argv[1] if len(sys.argv) > 1 else "orders"
    conn = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    consume_with_backoff(conn.channel(), queue)
