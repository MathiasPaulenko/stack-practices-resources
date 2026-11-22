# Comunicación entre Microservicios — ejemplos complementarios

Esta carpeta contiene ejemplos ejecutables de comunicación síncrona y
asíncrona para la receta de StackPractices
[Patrones de Comunicación entre Microservicios](https://stackpractices.com/es/recipes/microservices-communication/).

## Archivos

| Archivo | Descripción |
| --- | --- |
| `rest_client.py` | Llamada REST en Python con `httpx` + reintentos `tenacity` y timeout |
| `rest_client.mjs` | Llamada REST en Node.js con `fetch` y timeout de 5s con `AbortController` |
| `rabbitmq_producer.py` | Productor RabbitMQ que publica `orders.created` (`pika`, mensajes persistentes) |
| `dlq_consumer.py` | Consumidor con contador de reintentos y dead-letter queue `orders.created.dlq` |
| `requirements.txt` | Dependencias de Python |
| `kafka_producer.mjs` | Productor Kafka que publica `orders.created` (`kafkajs`) |
| `grpc_client.ts` | Cliente gRPC `OrderService` (`@grpc/grpc-js` + `@grpc/proto-loader`) |
| `proto/orders.proto` | Contrato Protobuf usado por el cliente gRPC |
| `package.json` | Dependencias y scripts de Node |
| `pom.xml` | Proyecto Maven para los ejemplos de Java |
| `src/main/java/OrderRestClient.java` | Llamada REST con `RestTemplate` de Spring |
| `src/main/java/ResilientPaymentClient.java` | Circuit breaker + retry de Resilience4j sobre un gateway de pago |

## Cómo ejecutar los ejemplos

### Python

```bash
python -m venv .venv
source .venv/bin/activate  # o .venv\Scripts\activate en Windows
pip install -r requirements.txt
python rest_client.py         # necesita un endpoint HTTP de orders-service
python rabbitmq_producer.py   # necesita RabbitMQ en RABBITMQ_HOST (default rabbitmq)
python dlq_consumer.py        # necesita RabbitMQ en RABBITMQ_URL (default amqp://rabbitmq:5672)
```

### Node.js / TypeScript

```bash
npm install
npm run rest    # necesita un endpoint HTTP de orders-service
npm run kafka   # necesita Kafka en KAFKA_BROKERS (default kafka:9092)
npm run grpc    # necesita un servidor gRPC OrderService en orders-service:50051
```

### Java

```bash
mvn compile
# ResilientPaymentClient envuelve cualquier implementación de PaymentGateway
# con un circuit breaker (umbral de fallo 50%, 30s abierto) y 3 reintentos.
```

## Ver también

- [Reintentos y Backoff](https://stackpractices.com/es/recipes/retry-backoff/)
- [Patrón Circuit Breaker](https://stackpractices.com/es/recipes/circuit-breaker-pattern-recipe/)
- [Arquitectura Event-Driven](https://stackpractices.com/es/recipes/event-driven-architecture/)
