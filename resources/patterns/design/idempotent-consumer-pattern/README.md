# Idempotent Consumer Pattern — Companion Code

Companion code for the [Idempotent Consumer Pattern](https://stackpractices.com/patterns/idempotent-consumer-pattern/) guide on StackPractices.

## Files

| File | Description |
|------|-------------|
| `python_idempotent_consumer.py` | Python implementation with SQLite dedup store |
| `java_idempotent_consumer.java` | Java implementation with in-memory + repository dedup |
| `javascript_idempotent_consumer.js` | Node.js implementation with Redis dedup |
| `test_dedup.py` | Tests for deduplication logic (5 tests) |
| `test_idempotent_operations.py` | Tests for idempotent operations and crash recovery (4 tests) |

## Running

### Python

```bash
python python_idempotent_consumer.py
pytest test_dedup.py test_idempotent_operations.py -v
```

### Java

```bash
javac java_idempotent_consumer.java
java IdempotentConsumer
```

### JavaScript

```bash
node javascript_idempotent_consumer.js
```

## License

MIT
