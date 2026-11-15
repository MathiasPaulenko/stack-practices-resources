# Kafka Event Streaming — Companion Code

Runnable KafkaJS demo for the StackPractices recipe [Event Streaming with Apache Kafka and Node.js](https://stackpractices.com/recipes/kafka-event-streaming/).

## Files

| File | Purpose |
|---|---|
| `docker-compose.yml` | Single-node Kafka in KRaft mode (no Zookeeper) |
| `producer.js` | Publishes 10 `OrderCreated` events keyed by `userId` |
| `consumer.js` | `notification-service` group — sends poison messages to `orders.created.dlq` |
| `dlq-consumer.js` | Inspector that drains the DLQ and prints the attached error headers |
| `package.json` | `kafkajs` dependency + `produce`/`consume`/`consume-dlq` scripts |

## Run

```bash
docker compose up -d        # start Kafka (KRaft, localhost:9092)
npm install
npm run consume             # terminal 1
npm run consume-dlq         # terminal 2
npm run produce             # terminal 3 — sends 10 orders
```

Orders with `totalCents` ending in `500` are deliberately "poisoned": `consumer.js` throws inside the handler, republishes the message to `orders.created.dlq` with the error in an `x-error` header, and lets the offset advance. Watch them land in the DLQ inspector terminal.

## Notes

- `KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092` is host-only. To connect from another container, add a second listener (e.g. `PLAINTEXT://kafka:29092`).
- Topics auto-create on first produce. For production, create them explicitly with the partition count and replication factor you need.
- The DLQ keeps the original key, so failed messages stay ordered with the rest of the user's events.
