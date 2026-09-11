# Queue-Based Load Leveling Pattern — Companion Resources

This companion contains runnable implementations of the Queue-Based Load Leveling
pattern in Python, Java, and JavaScript.

## Files

| File | Language | Description |
|------|----------|-------------|
| `queue_producer.py` | Python | Bounded in-memory queue with depth limit, TTL, dead-letter queue, producer |
| `queue_consumer.py` | Python | Task handlers for email, report, and payment task types |
| `queue_config.java` | Java | Spring + RabbitMQ configuration with DLQ, TTL, and overflow |
| `queue_producer.js` | JavaScript | BullMQ producer with priority, backoff, and rate limiting |
| `queue_consumer.js` | JavaScript | BullMQ consumer with concurrency and rate limiting |
| `test_queue.py` | Python | 15 tests covering enqueue, dequeue, depth limits, TTL, DLQ, consumer |
| `test_queue.js` | JavaScript | 15 tests covering producer/consumer structure and configuration |

## Running the Python tests

```bash
python test_queue.py
```

Expected output:

```
=== All 15 tests passed ===
```

## Running the JavaScript tests

```bash
node test_queue.js
```

Expected output:

```
=== All 15 tests passed ===
```

## Key concepts

- **Depth limit**: Queue rejects new messages when `max_length` is reached.
- **Message TTL**: Stale messages expire and move to the dead-letter queue.
- **Dead-letter queue (DLQ)**: Failed messages after `max_retries` go here.
- **Rate limiting**: Consumer processes at a controlled rate to avoid overload.
- **Auto-scaling**: Monitor `queue.depth()` — if it rises, add more consumers.

## Source

- [Queue-Based Load Leveling Pattern](https://stackpractices.com/patterns/queue-based-load-leveling-pattern/)
