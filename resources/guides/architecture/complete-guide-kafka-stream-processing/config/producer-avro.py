"""Avro producer with Schema Registry from the guide."""
from confluent_kafka import SerializingProducer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer

schema_registry_client = SchemaRegistryClient({"url": "http://localhost:8081"})

schema_str = """
{
  "type": "record",
  "name": "Order",
  "fields": [
    {"name": "order_id", "type": "int"},
    {"name": "amount", "type": "double"},
    {"name": "status", "type": "string"}
  ]
}
"""

avro_serializer = AvroSerializer(schema_registry_client, schema_str)

producer = SerializingProducer({
    "bootstrap.servers": "localhost:9092",
    "key.serializer": "org.apache.kafka.common.serialization.StringSerializer",
    "value.serializer": avro_serializer,
})

producer.produce(topic="orders-avro", key="order-1",
                 value={"order_id": 1, "amount": 99.99, "status": "created"})
producer.flush()
