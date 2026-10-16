"""Kafka producer/consumer with W3C trace context propagation via message headers."""
import json

from kafka import KafkaConsumer, KafkaProducer
from opentelemetry import propagate, trace

tracer = trace.get_tracer(__name__)

producer = KafkaProducer(bootstrap_servers=["localhost:9092"])
consumer = KafkaConsumer("orders", bootstrap_servers=["localhost:9092"])


def send_event(topic: str, event: dict) -> None:
    """Inject the current trace context into Kafka message headers."""
    headers: dict[str, str] = {}
    propagate.inject(headers)

    kafka_headers = [(k, v.encode("utf-8")) for k, v in headers.items()]
    producer.send(
        topic,
        value=json.dumps(event).encode("utf-8"),
        headers=kafka_headers,
    )
    producer.flush()


def consume_events() -> None:
    """Extract the producer's context so consumer spans join the same trace."""
    for message in consumer:
        headers = {k: v.decode("utf-8") for k, v in message.headers}
        ctx = propagate.extract(headers)

        with tracer.start_as_current_span("process_event", context=ctx):
            event = json.loads(message.value)
            process_order_event(event)


def process_order_event(event: dict) -> None:  # pragma: no cover
    raise NotImplementedError("Wire in your order event handling here.")
