# Sequential Convoy Pattern — Companion Resources

Runnable implementations of the Sequential Convoy pattern in Python, Java, and
JavaScript. Each one simulates a partitioned broker in memory, so they run
without Kafka, Service Bus, or Redis.

## Files

| File | Language | Description |
|------|----------|-------------|
| `convoy_processor.py` | Python | Partition router, per-entity sequence numbers, ordered consumer with gap buffering |
| `ConvoyProcessor.java` | Java | Same simulation: `PartitionedBroker`, `ConvoyProducer`, `ConvoyConsumer` |
| `convoy_processor.js` | JavaScript | Same simulation with `Map`-based sequence tracking and private methods |

## Running the examples

```bash
python convoy_processor.py
javac ConvoyProcessor.java && java ConvoyProcessor
node convoy_processor.js
```

Each script produces three events for `user-123`, delivers them out of order
(sequence 3 before 2), and asserts the consumer still applies them in order.

## Key concepts

- **Partition key**: events for the same entity hash to the same partition, so a
  single consumer owns them.
- **Sequence numbers**: producers attach a per-entity counter; consumers use it
  to detect gaps and duplicates.
- **Gap buffering**: out-of-order events wait in a per-entity buffer until the
  missing sequence numbers arrive.

## Source

Companion to the StackPractices article:
<https://stackpractices.com/patterns/sequential-convoy-pattern/>
