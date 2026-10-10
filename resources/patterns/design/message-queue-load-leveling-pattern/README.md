# Message Queue Load Leveling — companion examples

Runnable examples for the StackPractices pattern
[Message Queue Load Leveling](https://stackpractices.com/patterns/message-queue-load-leveling-pattern/):
the producer writes at any rate and the consumer drains the queue at a controlled pace.

## Files

| File | Description |
| --- | --- |
| `celery_consumer.py` | Celery producer + task on Redis — burst 1,000 orders, worker drains 1 every 2 s |
| `requirements.txt` | Python dependency (`celery[redis]`) |
| `bullmq_worker.mjs` | BullMQ queue + worker with `limiter` (max 1 job / 2 s) on Redis |
| `package.json` | Node dependency (`bullmq`) and run script |
| `pom.xml` | Maven project for the Java example |
| `src/main/java/OrderProcessor.java` | Spring AMQP producer + `@RabbitListener` consumer with `concurrency=1` |

## Running the examples

### Python (Celery + Redis)

```bash
docker run -p 6379:6379 -d redis
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
celery -A celery_consumer worker --concurrency=1 --loglevel=info   # terminal 1
python celery_consumer.py                                        # terminal 2
```

### Node.js (BullMQ + Redis)

```bash
docker run -p 6379:6379 -d redis
npm install
npm start
```

### Java (Spring AMQP + RabbitMQ)

```bash
docker run -p 5672:5672 -d rabbitmq
mvn compile exec:java -Dexec.mainClass="OrderProcessor"
```

## Notes

- The examples need a running broker (Redis for Celery/BullMQ, RabbitMQ for Java).
- Watch the queue: the burst enqueues 1,000 jobs instantly while the worker
  drains them at its own rate — that rate mismatch is the whole pattern.
