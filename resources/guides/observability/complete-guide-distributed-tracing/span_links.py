"""Span links: associate traces without nesting for Kafka batch consumers."""
import json

from kafka import KafkaConsumer
from opentelemetry import propagate, trace
from opentelemetry.trace import Link

tracer = trace.get_tracer(__name__)

consumer = KafkaConsumer("orders", bootstrap_servers=["localhost:9092"])


def consume_batch() -> None:
    """Start one span per message, linked to the producer's context.

    A batch consumer parenting N messages to one span produces ugly fan-in
    traces. Links keep each message as its own trace while preserving the
    causal relationship in the backend UI.
    """
    for message in consumer:
        headers = {k: v.decode("utf-8") for k, v in message.headers}
        ctx = propagate.extract(headers)

        # Extract the producer's span context to link (not parent) the span
        producer_span = trace.get_current_span(ctx)
        links = [Link(producer_span.get_span_context())]

        with tracer.start_as_current_span("process_event", links=links):
            event = json.loads(message.value)
            process_order_event(event)


def process_order_event(event: dict) -> None:  # pragma: no cover
    raise NotImplementedError("Wire in your order event handling here.")
