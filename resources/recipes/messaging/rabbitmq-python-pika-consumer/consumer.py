"""RabbitMQ consumer with manual acknowledgments, prefetch=1 fair dispatch,
and header-based retry tracking before dead-lettering."""

import json
import sys
import time

import pika

from producer import get_connection

MAX_RETRIES = 3


def process_task(message: dict) -> None:
    if message["type"] == "email":
        send_email(message["payload"])
    elif message["type"] == "report":
        generate_report(message["payload"])
    else:
        raise ValueError(f"Unknown task type: {message['type']}")


def send_email(payload: dict) -> None:
    print(f"Sending email to {payload['to']}")
    time.sleep(1)


def generate_report(payload: dict) -> None:
    print(f"Generating report {payload}")
    time.sleep(1)


def process_message(channel, method, properties, body):
    message = json.loads(body)
    headers = properties.headers or {}
    retry_count = headers.get("x-retry-count", 0)
    print(f"Received: {message['id']} — {message['type']}")

    try:
        process_task(message)
        channel.basic_ack(delivery_tag=method.delivery_tag)
        print(f"Done: {message['id']}")
    except Exception as e:
        print(f"Failed: {message['id']} — {e}")
        if retry_count < MAX_RETRIES:
            print(f"Retry {retry_count + 1}/{MAX_RETRIES} for {message['id']}")
            channel.basic_publish(
                exchange="",
                routing_key=method.routing_key,
                body=body,
                properties=pika.BasicProperties(
                    delivery_mode=2,
                    headers={"x-retry-count": retry_count + 1},
                    content_type="application/json",
                ),
            )
            channel.basic_ack(delivery_tag=method.delivery_tag)
        else:
            print(f"Max retries exceeded for {message['id']}, sending to DLQ")
            channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)


def start_consumer(queue_name: str, host: str = "localhost") -> None:
    connection = get_connection(host)
    channel = connection.channel()
    channel.queue_declare(queue=queue_name, durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue_name, on_message_callback=process_message)
    print(f"Waiting for messages on {queue_name}. To exit press CTRL+C")
    channel.start_consuming()


if __name__ == "__main__":
    start_consumer(sys.argv[1] if len(sys.argv) > 1 else "task_queue")
