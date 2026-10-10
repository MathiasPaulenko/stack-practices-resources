# Event-Driven Architecture — companion examples

This folder contains runnable producer and consumer examples for the
StackPractices recipe
[Design Event-Driven Systems with Event Buses and Brokers](https://stackpractices.com/recipes/event-driven-architecture/).

## Files

| File | Description |
| --- | --- |
| `kafka_publisher.py` | Python producer that publishes `OrderPlaced` to Kafka (`kafka-python`, `acks=all`) |
| `schema_registry_avro.py` | Avro-serialized producer with Confluent Schema Registry and delivery callback |
| `requirements.txt` | Python dependencies |
| `rabbitmq_consumer.mjs` | Node.js consumer with manual acks and dead-lettering (`amqplib`) |
| `eventbridge_producer.mjs` | Publish to AWS EventBridge and consume from its SQS target |
| `package.json` | Node dependencies and scripts |
| `eventbridge.tf` | Terraform event bus + rule + targets (SQS and Lambda) |
| `pom.xml` | Maven project for the Java example |
| `src/main/java/OrderEventStore.java` | Kafka Streams event sourcing with a queryable state store |

## Running the examples

### Python

```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
python kafka_publisher.py      # needs a Kafka broker at kafka:9092
python schema_registry_avro.py # also needs Schema Registry at :8081
```

### Node.js

```bash
npm install
npm run rabbitmq    # needs RabbitMQ at amqp://rabbitmq
npm run eventbridge # needs AWS credentials and INVENTORY_QUEUE_URL
```

### Java

```bash
mvn compile
mvn exec:java -Dexec.mainClass="OrderEventStore"
```

The `pom.xml` uses Java 17 and Kafka Streams 3.7.1. Domain types
(`OrderEvent`, `OrderEventSerde`, `OrderStateSerde`, `getStreamsConfig`)
are stubs — wire your own serialization and broker config.

### Terraform

```bash
terraform init
terraform plan   # add aws_sqs_queue.inventory_queue and a Lambda first
```

## Notes

- All examples expect running infrastructure (Kafka broker, RabbitMQ,
  AWS account). They are reference implementations for the recipe, not
  turnkey deployments.
- `save_order()` / `reserveInventory()` are intentionally left as stubs —
  plug in your persistence or inventory service.
