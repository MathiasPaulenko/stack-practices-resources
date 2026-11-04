# Complete Guide to Apache Kafka in Production — Companion

Runnable companion for the StackPractices guide
[Complete Guide to Apache Kafka in Production](https://stackpractices.com/guides/complete-guide-kafka-production/).

- `docker-compose.yml` — 3-broker KRaft cluster (no ZooKeeper) matching production RF=3
- `config/server-production.properties` — production broker settings (RF=3, ISR=2, retention)
- `config/producer-tuning.py` / `consumer-tuning.py` — tuned kafka-python clients from the guide
- `scripts/create-topics.sh` — creates the `orders` topic (RF=3, matches the 3-broker cluster)
- `scripts/check-health.sh` — under-replicated partitions + consumer lag checks

## Run

```bash
docker compose up -d
./scripts/create-topics.sh
pip install kafka-python
python config/producer-tuning.py
```

Kill `kafka3` to watch a partition leader fail over to an ISR replica — the failure scenario covered in the guide.
