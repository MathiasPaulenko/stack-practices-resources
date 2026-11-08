# Dead Letter Queue Runbook — Runnable Simulation

Companion to the StackPractices doc [Dead Letter Queue Runbook](https://stackpractices.com/docs/dead-letter-queue-runbook/).

An end-to-end DLQ operations demo in three equivalent implementations: an in-memory broker where a poison message retries three times, lands in the DLQ with failure metadata, gets inspected and categorized, then replays back to the source queue after the "fix" deploys — the full runbook lifecycle in one run. Stdlib only, no dependencies.

## Files

| File | Stack | Run |
| --- | --- | --- |
| `src/dlq_runbook_simulation.py` | Python 3.9+ (stdlib only) | `python src/dlq_runbook_simulation.py` |
| `src/dlq-runbook-simulation.js` | Node.js 14+ (stdlib only) | `node src/dlq-runbook-simulation.js` |
| `src/DlqRunbookSimulation.java` | Java 11+ | `javac src/DlqRunbookSimulation.java -d out && java -cp out DlqRunbookSimulation` |

Each run prints the four phases: consume (poison retries then dead-letters), DLQ inspection with error categorization, replay after the fix deploys, and post-replay verification with empty queues.

The broker is an in-memory stub so the demo runs anywhere; in production you'd swap it for RabbitMQ (dead letter exchange), Kafka (error topic), or SQS (redrive policy) — the retry/inspect/replay logic stays identical.
