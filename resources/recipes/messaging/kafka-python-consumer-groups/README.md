# Kafka Consumer Groups (Python) — Companion Code

Runnable consumer-group demo for the StackPractices recipe [Kafka Consumer Groups with Python](https://stackpractices.com/recipes/kafka-python-consumer-groups/).

## Files

| File | Purpose |
|---|---|
| `docker-compose.yml` | Single-node Kafka in KRaft mode (no Zookeeper) |
| `producer.py` | Sends 30 `OrderCreated` events keyed by `userId` |
| `consumer_worker.py` | Consumer-group member with `on_assign`/`on_revoke`/`on_lost` logging |
| `requirements.txt` | `confluent-kafka` dependency |

## Run

```bash
docker compose up -d          # start Kafka (KRaft, localhost:9092)
pip install -r requirements.txt

python consumer_worker.py worker-1   # terminal 1
python consumer_worker.py worker-2   # terminal 2 — watch the rebalance logs
python producer.py                   # terminal 3 — sends 30 orders
```

Then experiment:

- Start a `worker-3` — cooperative-sticky moves partitions incrementally instead of stopping the group.
- Ctrl+C a worker — its partitions get reassigned after `session.timeout.ms`.
- Re-run `producer.py` while a worker is down — the resumed worker catches up from its last committed offset.

## Notes

- `KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092` is host-only; containers need a second internal listener.
- The `orders` topic auto-creates with a default partition count. For a real rebalance demo, create it with several partitions first: `docker exec kafka kafka-topics --create --topic orders --partitions 6 --bootstrap-server localhost:9092`.
- `consumer.commit(msg)` commits per message for demo clarity; batch commits for throughput in production.
