"""Publish OrderPlaced events serialized with Avro and Schema Registry."""
import uuid
from dataclasses import asdict, dataclass

from confluent_kafka import SerializingProducer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer

schema_registry_client = SchemaRegistryClient(
    {"url": "http://schema-registry:8081"}
)

ORDER_EVENT_SCHEMA = """
{
  "type": "record",
  "name": "OrderEvent",
  "namespace": "com.stackpractices.events",
  "fields": [
    {"name": "event_id", "type": "string"},
    {"name": "event_type", "type": "string"},
    {"name": "aggregate_id", "type": "string"},
    {"name": "customer_id", "type": "string"},
    {"name": "total", "type": "double"},
    {"name": "items", "type": {"type": "array", "items": "string"}},
    {"name": "occurred_at", "type": "string"}
  ]
}
"""

avro_serializer = AvroSerializer(
    schema_registry_client,
    ORDER_EVENT_SCHEMA,
    lambda obj, ctx: asdict(obj),
)


@dataclass
class OrderEvent:
    event_id: str
    event_type: str
    aggregate_id: str
    customer_id: str
    total: float
    items: list
    occurred_at: str


producer = SerializingProducer(
    {
        "bootstrap.servers": "kafka:9092",
        "value.serializer": avro_serializer,
    }
)


def delivery_report(err, msg):
    # Called once the broker acks (or rejects) the message
    if err is not None:
        print(f"Delivery failed: {err}")


def publish_order_event(order):
    event = OrderEvent(
        event_id=str(uuid.uuid4()),
        event_type="OrderPlaced",
        aggregate_id=order.id,
        customer_id=order.customer_id,
        total=order.total(),
        items=[item.id for item in order.items],
        occurred_at=order.created_at.isoformat(),
    )
    producer.produce(
        topic="orders",
        key=order.id.encode(),
        value=event,
        on_delivery=delivery_report,
    )
    producer.flush()
