"""Kafka consumer with Avro deserialization via Confluent Schema Registry."""
from confluent_kafka import DeserializingConsumer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer
from confluent_kafka.serialization import StringDeserializer

schema_registry_client = SchemaRegistryClient({"url": "http://localhost:8081"})

avro_deserializer = AvroDeserializer(schema_registry_client)

consumer = DeserializingConsumer({
    "bootstrap.servers": "localhost:9092",
    "group.id": "customer-processor",
    "auto.offset.reset": "earliest",
    "key.deserializer": StringDeserializer("utf_8"),
    "value.deserializer": avro_deserializer,
})

consumer.subscribe(["customer-events"])

while True:
    msg = consumer.poll(1.0)
    if msg is None:
        continue
    if msg.error():
        print(f"Consumer error: {msg.error()}")
        continue

    customer = msg.value()
    print(f"Received: id={customer['id']}, email={customer['email']}, status={customer['status']}")

    # v1 consumers won't have 'phone' or 'country' — they get the schema defaults
    phone = customer.get("phone", "N/A")
    country = customer.get("country", "US")
    print(f"  phone={phone}, country={country}")

    consumer.commit(msg)
