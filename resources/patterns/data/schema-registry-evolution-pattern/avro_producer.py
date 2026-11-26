"""Kafka producer with Avro serialization via Confluent Schema Registry."""
import json

from confluent_kafka import SerializingProducer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.serialization import StringSerializer

schema_registry_client = SchemaRegistryClient({"url": "http://localhost:8081"})

with open("customer-v2.avsc") as f:
    schema_str = json.dumps(json.load(f))

avro_serializer = AvroSerializer(
    schema_registry_client,
    schema_str,
    lambda obj, ctx: obj,
)

producer = SerializingProducer({
    "bootstrap.servers": "localhost:9092",
    "key.serializer": StringSerializer("utf_8"),
    "value.serializer": avro_serializer,
})


def delivery_report(err, msg):
    if err:
        print(f"Delivery failed: {err}")
    else:
        print(f"Delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")


if __name__ == "__main__":
    customer_event = {
        "id": 42,
        "email": "alice@example.com",
        "status": "active",
        "created_at": 1783305600000,
        "phone": "555-1234",
        "country": "US",
    }
    producer.produce(
        topic="customer-events",
        key=str(customer_event["id"]),
        value=customer_event,
        on_delivery=delivery_report,
    )
    producer.flush()
