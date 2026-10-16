# tests/integration/test_kafka.py — Kafka with Testcontainers
import pytest
from testcontainers.kafka import KafkaContainer
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError
import json

@pytest.fixture(scope="module")
def kafka_container():
    with KafkaContainer() as kafka:
        yield kafka

@pytest.fixture
def producer(kafka_container):
    p = KafkaProducer(
        bootstrap_servers=kafka_container.get_bootstrap_server(),
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        key_serializer=lambda k: k.encode("utf-8") if k else None,
    )
    yield p
    p.close()

@pytest.fixture
def consumer(kafka_container):
    c = KafkaConsumer(
        "test-topic",
        bootstrap_servers=kafka_container.get_bootstrap_server(),
        auto_offset_reset="earliest",
        group_id="test-group",
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        consumer_timeout_ms=10000,
    )
    yield c
    c.close()

def test_produce_and_consume(producer, consumer):
    producer.send("test-topic", key="key1", value={"message": "hello"})
    producer.flush()

    records = list(consumer)
    assert len(records) >= 1
    assert records[-1].key == "key1"
    assert records[-1].value == {"message": "hello"}
