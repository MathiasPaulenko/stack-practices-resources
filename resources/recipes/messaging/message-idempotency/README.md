# Message Processing Idempotency — Companion

Runnable examples for the StackPractices recipe [Message Processing Idempotency](https://stackpractices.com/recipes/message-idempotency/).

## What is here

- `redis_dedup.js` — idempotent payment webhook with Node.js and Redis `SET NX EX`.
- `postgres_dedup.sql` — PostgreSQL table and a sample transaction that inserts the message ID and updates the side effect.
- `kafka_consumer.py` — Python Kafka consumer with Redis deduplication.
- `kafka_consumer.java` — Java Kafka consumer with Redis deduplication.
- `kafka_idempotent_producer.java` — Java Kafka idempotent producer config.
- `sqs_handler.py` — AWS SQS FIFO consumer with conditional write against DynamoDB.
- `docker-compose.yml` — starts Redis, PostgreSQL and a single-node Kafka locally.
- `package.json`, `requirements.txt`, `pom.xml` — minimal dependencies.

## Quick start

1. Start the infrastructure:

```bash
docker compose up -d
```

2. Run the Node.js Redis example:

```bash
cp .env.example .env
npm install
node redis_dedup.js
```

3. Run the Python Kafka consumer:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python kafka_consumer.py
```

4. Run the Java Kafka consumer:

```bash
mvn compile
mvn exec:java -Dexec.mainClass="KafkaConsumerDedup"
```

## Notes

- The examples use `localhost` and default ports. Update them for your environment.
- The Redis examples set a `processing` state and delete it on error. Only delete the key if no side effect completed.
- Kafka's idempotent producer covers retries per partition, not rebalances or producer restarts. The consumer still needs its own dedup store.
