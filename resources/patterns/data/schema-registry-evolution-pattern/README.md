# Schema Registry Evolution — Companion Resources

Runnable files for the [Schema Registry Evolution](https://stackpractices.com/patterns/schema-registry-evolution-pattern/) pattern on StackPractices.

## Files

| File | What it is |
|------|------------|
| `customer-v1.avsc` | Avro schema v1 for `customer-events` (id, email, status enum, created_at). |
| `customer-v2.avsc` | Backward-compatible v2: new `suspended` enum symbol plus optional `phone` and `country` fields with defaults. |
| `customer.proto` | The same evolution expressed in Protobuf (`optional` fields, new enum value). |
| `register_schema.py` | Registers both Avro versions against a subject via the Schema Registry REST API. |
| `compatibility.py` | Sets subject compatibility (`BACKWARD`/`FORWARD`/`FULL`) and dry-checks a new schema against the latest version — the call you wire into CI. |
| `avro_producer.py` | `SerializingProducer` publishing a v2 customer event through `AvroSerializer`. |
| `avro_consumer.py` | `DeserializingConsumer` that resolves the schema id from the wire format and shows how v1 consumers get defaults for v2 fields. |
| `CustomerProducer.java` | Same producer flow with `KafkaAvroSerializer` and a generated `Customer` class. |

## Usage

You need Kafka + Schema Registry running (e.g. `docker compose up` on the Confluent stack), then:

```bash
pip install requests confluent-kafka
python register_schema.py          # registers v1 and v2
python compatibility.py            # sets BACKWARD and checks v2 against it
python avro_producer.py            # publishes a v2 event
python avro_consumer.py            # consumes with the registry-resolved schema
```

The Java example needs the generated `Customer`/`Status` classes — build them from `customer-v2.avsc` with `avro-tools` or the Avro Maven/Gradle plugin.
