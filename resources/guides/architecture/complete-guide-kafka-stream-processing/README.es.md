# Guía Completa de Kafka Stream Processing — Companion

Companion ejecutable de la guía de StackPractices
[Guía Completa de Kafka Stream Processing](https://stackpractices.com/es/guides/complete-guide-kafka-stream-processing/).

- `docker-compose.yml` — cluster KRaft de 3 brokers + Confluent Schema Registry
- `src/main/java/OrderStreamProcessor.java` — la topología de Streams (branch, filter, count con ventanas, exactly_once_v2)
- `config/producer-aiokafka.py` / `consumer-kafkajs.js` — clientes de la guía
- `config/producer-avro.py` — producer Avro con Schema Registry
- `config/jdbc-source-connector.json` / `elasticsearch-sink-connector.json` — configs de Connect
- `scripts/create-topics.sh` — crea todos los topics de la topología con RF=3

## Ejecutar

```bash
docker compose up -d
./scripts/create-topics.sh
pip install aiokafka && python config/producer-aiokafka.py
# Compila y corre la app de Streams con tu setup habitual de Maven/Gradle
```
