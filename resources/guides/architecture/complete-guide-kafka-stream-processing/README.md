# Complete Guide to Kafka Stream Processing — Companion

Runnable companion for the StackPractices guide
[Complete Guide to Kafka Stream Processing](https://stackpractices.com/guides/complete-guide-kafka-stream-processing/).

- `docker-compose.yml` — 3-broker KRaft cluster + Confluent Schema Registry
- `src/main/java/OrderStreamProcessor.java` — the Streams topology (branch, filter, windowed count, exactly_once_v2)
- `config/producer-aiokafka.py` / `consumer-kafkajs.js` — clients from the guide
- `c
