"""Trace-context propagation across a RabbitMQ boundary.

The producer injects ``traceparent`` into the message headers; the
consumer extracts it before starting its span, so the async work stays
attached to the original request's trace.

Needs a local broker: ``docker run -p 5672:5672 rabbitmq:3``.
Run ``python rabbitmq_propagation.py`` for a producer+consumer demo.
"""

import json
import threading
import time

import pika
from opentelemetry import propagate, trace

from otel_setup import init_tracing

tracer = init_tracing("orders-worker")
QUEUE = "orders"


def _channel() -> pika.adapters.blocking_connection.BlockingChannel:
    connection = pika.BlockingConnection(
        pika.ConnectionParameters("localhost")
    )
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE)
    return channel


def publish_order_event(order_data: dict) -> None:
    """Publish an order event with the trace context in the headers."""
    with tracer.start_as_current_span("publish_order_event"):
        headers: dict[str, str] = {}
        propagate.inject(headers)

        channel = _channel()
        channel.basic_publish(
            exchange="",
            routing_key=QUEUE,
            body=json.dumps(order_data),
            properties=pika.BasicProperties(headers=headers),
        )
        channel.connection.close()


def consume_order_events(stop_after: int | None = None) -> None:
    """Consume order events, extracting context so spans join the trace."""
    channel = _channel()
    consumed = 0

    def callback(ch, method, properties, body):
        nonlocal consumed
        ctx = propagate.extract(properties.headers or {})
        with tracer.start_as_current_span(
            "process_order_event", context=ctx
        ) as span:
            order = json.loads(body)
            span.set_attribute("order.id", order.get("order_id", "unknown"))
            print(f"processing order {order}")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        consumed += 1
        if stop_after is not None and consumed >= stop_after:
            channel.stop_consuming()

    channel.basic_consume(queue=QUEUE, on_message_callback=callback)
    channel.start_consuming()


if __name__ == "__main__":
    consumer = threading.Thread(
        target=consume_order_events, kwargs={"stop_after": 1}, daemon=True
    )
    consumer.start()
    time.sleep(0.5)  # let the consumer declare and bind
    publish_order_event({"order_id": "ord_42", "amount": 99.0})
    consumer.join(timeout=10)
    trace.get_tracer_provider().shutdown()  # flush spans before exit
