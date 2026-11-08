# Dead Letter Channel Pattern — Runnable Implementations

Companion to the StackPractices pattern [Dead Letter Channel Pattern](https://stackpractices.com/patterns/dead-letter-channel-pattern/).

A dead letter channel demo in three equivalent implementations: an in-memory broker with a main queue, a retry queue, and a dead letter queue (DLQ). The consumer processes orders; one message arrives with a missing `order_id` (a poison message), fails on every attempt, exhausts its retry budget of 3, and lands in the DLQ with failure metadata attached. Stdlib only — no dependencies needed.

## Files

| File | Stack | Run |
| --- | --- | --- |
| `src/dead_letter_channel.py` | Python 3.9+ (stdlib only) | `python src/dead_letter_channel.py` |
| `src/dead-letter-channel.js` | Node.js 14+ (stdlib only) | `node src/dead-letter-channel.js` |
| `src/DeadLetterChannel.java` | Java 16+ (`record`) | `javac src/DeadLetterChannel.java && java -cp src DeadLetterChannel` |

Each run prints the two healthy orders being processed, the poison message retrying and moving to the DLQ, the final queue depths, and a replay step that repairs the payload and re-queues it.

The broker here is an in-memory stub so the demo runs anywhere; in production you'd swap `Broker` for SQS (redrive policy), RabbitMQ (dead letter exchange) or a Kafka error topic — the retry/DLQ/replay logic stays identical.
