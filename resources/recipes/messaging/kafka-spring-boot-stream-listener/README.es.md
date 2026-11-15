# Kafka Stream Listener con Spring Boot

App Spring Boot 3 ejecutable que consume el tópico `orders` con `@KafkaListener`, acknowledgment manual, reintentos no bloqueantes vía `@RetryableTopic` y un sink dead-letter con `@DltHandler`. Incluye un broker Kafka de un nodo en modo KRaft.

Companion de: https://stackpractices.com/es/recipes/kafka-spring-boot-stream-listener/

## Requisitos

- Java 17+
- Maven 3.8+
- Docker + Docker Compose

## Ejecución

```bash
docker compose up -d          # levanta el broker
mvn spring-boot:run           # arranca la app
```

Al arrancar, `SampleOrderProducer` envía 20 registros `OrderEvent` a `orders`. Cada 7º evento lleva un total negativo, falla la validación del listener, reintenta con backoff exponencial (`orders-retry-0` → `-retry-1` → `-retry-2`) y finalmente cae en `orders-dlt`, donde `@DltHandler` lo registra.

## Qué mirar

- `OrderConsumer` — `@RetryableTopic` + `@KafkaListener` + `Acknowledgment` + `@DltHandler`
- `application.yml` — `enable-auto-commit: false`, `ack-mode: manual`, `concurrency: 3`, trusted packages
- `SampleOrderProducer` — registros JSON con clave vía `KafkaTemplate`

## Inspeccionar la DLT

```bash
docker exec -it <kafka-container> kafka-console-consumer \
  --bootstrap-server localhost:9092 --topic orders-dlt \
  --from-beginning --property print.headers=true
```
