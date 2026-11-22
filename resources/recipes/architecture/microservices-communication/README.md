# Microservices Communication — companion examples

This folder contains runnable sync/async communication examples for the
StackPractices recipe
[Microservices Communication Patterns](https://stackpractices.com/recipes/microservices-communication/).

## Files

| File | Description |
| --- | --- |
| `rest_client.py` | Python REST call with `httpx` + `tenacity` retries and timeout |
| `rest_client.mjs` | Node.js REST call with `fetch` and a 5s `AbortController` timeout |
| `rabbitmq_producer.py` | RabbitMQ producer publishing `orders.created` (`pika`, persistent messages) |
| `dlq_consumer.py` | Consumer with retry counter and dead-letter queue `orders.created.dlq` |
| `requirements.txt` | Python dependencies |
| `kafka_producer.mjs` | Kafka producer publishing `orders.created` (`kafkajs`) |
| `grpc_client.ts` | gRPC `OrderService` client (`@grpc/grpc-js` + `@grpc/proto-loader`) |
| `proto/orders.proto` | Protobuf contract used by the gRPC client |
| `package.json` | Node dependencies and scripts |
| `pom.xml` | Maven project for the Java examples |
| `src/main/java/OrderRestClient.java` | REST call with Spring `RestTemplate` |
| `src/main/java/ResilientPaymentClient.java` | Resilience4j circuit breaker + retry around a payment gateway |

## Running the examples

### Python

```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
python rest_client.py         # needs an orders-service HTTP endpoint
python rabbitmq_producer.py   # needs RabbitMQ at RABBITMQ_HOST (default rabbitmq)
python dlq_consumer.py        # needs RabbitMQ at RABBITMQ_URL (default amqp://rabbitmq:5672)
```

### Node.js / TypeScript

```bash
npm install
npm run rest    # needs an orders-service HTTP endpoint
npm run kafka   # needs Kafka at KAFKA_BROKERS (default kafka:9092)
npm run grpc    # needs an OrderService gRPC server at orders-service:50051
```

### Java

```bash
mvn compile
# ResilientPaymentClient wraps any PaymentGateway implementation with a
# circuit breaker (50% failure threshold, 30s open) and 3 retries.
```

## See also

- [Retry and Backoff](https://stackpractices.com/recipes/retry-backoff/)
- [Circuit Breaker Pattern](https://stackpractices.com/recipes/circuit-breaker-pattern-recipe/)
- [Event-Driven Architecture](https://stackpractices.com/recipes/event-driven-architecture/)
