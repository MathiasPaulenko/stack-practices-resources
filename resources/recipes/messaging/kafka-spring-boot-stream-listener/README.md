# Kafka Stream Listener with Spring Boot

Runnable Spring Boot 3 app that consumes the `orders` topic with `@KafkaListener`, manual acknowledgment, non-blocking retries via `@RetryableTopic`, and a `@DltHandler` dead-letter sink. Includes a single-node Kafka broker in KRaft mode.

Companion to: https://stackpractices.com/recipes/kafka-spring-boot-stream-listener/

## Requirements

- Java 17+
- Maven 3.8+
- Docker + Docker Compose

## Run

```bash
docker compose up -d          # start the broker
mvn spring-boot:run           # start the app
```

On startup, `SampleOrderProducer` sends 20 `OrderEvent` records to `orders`. Every 7th event carries a negative total, fails validation in the listener, retries with exponential backoff (`orders-retry-0` → `-retry-1` → `-retry-2`), and finally lands in `orders-dlt`, where `@DltHandler` logs it.

## What to look at

- `OrderConsumer` — `@RetryableTopic` + `@KafkaListener` + `Acknowledgment` + `@DltHandler`
- `application.yml` — `enable-auto-commit: false`, `ack-mode: manual`, `concurrency: 3`, trusted packages
- `SampleOrderProducer` — keyed JSON records via `KafkaTemplate`

## Inspect the DLT

```bash
docker exec -it <kafka-container> kafka-console-consumer \
  --bootstrap-server localhost:9092 --topic orders-dlt \
  --from-beginning --property print.headers=true
```
