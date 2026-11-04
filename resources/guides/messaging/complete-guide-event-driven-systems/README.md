# Complete Guide to Event-Driven Systems — Companion Assets

Runnable artifacts from the
[Complete Guide to Event-Driven Systems](https://stackpractices.com/guides/complete-guide-event-driven-systems/).

## Contents

| File | What it shows |
| --- | --- |
| `outbox.sql` | Postgres outbox table + relay index + cleanup note |
| `saga_orchestrator.py` | Orchestration saga with compensation flow |
| `idempotent_consumer.py` | Redis `SETNX` dedup consumer pattern |
| `dlq_worker.py` | Retry counter + dead letter queue routing |
| `docker-compose.yml` | Redis + Postgres playground with outbox table |

## Usage

```bash
docker compose up -d   # start Redis + Postgres (outbox table auto-created)
```
