# Patrones de Comunicación entre Microservicios — Companion

Código companion de la [Guía Completa de Comunicación entre Microservicios](https://stackpractices.com/es/guides/complete-guide-microservices-communication/).

## Descripción

Los snippets de la guía como archivos independientes, organizados por patrón. Cada carpeta corresponde a una sección de la guía — son ejemplos mínimos y autocontenidos, no un sistema desplegable completo.

## Estructura

```text
rest/
└── orders_summary.py      # Servicio FastAPI que agrega dos llamadas upstream (httpx + timeout)
grpc/
├── order.proto            # Contrato Protobuf de OrderService
└── order_client.py        # Llamada con stub gRPC
queue/
└── order_events.py        # Cola durable RabbitMQ (pika), productor + consumidor con ack
pubsub/
└── order_events.js        # Productor KafkaJS + consumidor con consumer group
outbox/
├── OrderService.java      # Spring: escritura de negocio + fila outbox en una transacción
└── OutboxPublisher.java   # Relevo programado de la tabla outbox a Kafka
gateway/
└── kong.yaml              # Rutas Kong + plugins de rate-limiting y JWT
mesh/
└── order-service.yaml     # VirtualService Istio canary 90/10 + DestinationRule outlierDetection
resilience/
└── payment_client.py      # POST httpx con cabecera Idempotency-Key y timeouts
```

## Requisitos

Por ejemplo:

- `rest/`, `queue/`, `resilience/`: Python 3.9+, `fastapi`, `httpx`, `pika`
- `grpc/`: `grpcio`, `grpcio-tools` — genera los stubs con `python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. order.proto`
- `pubsub/`: Node.js 18+, `kafkajs`
- `outbox/`: Java 17+, Spring Boot, Spring Kafka (requiere una clase `Order` y una tabla `outbox`)
- `gateway/`: Kong Gateway (configuración declarativa)
- `mesh/`: Kubernetes + Istio

## Uso

Ejecuta cada archivo contra su propia infraestructura (un contenedor RabbitMQ para `queue/`, un broker Kafka para `pubsub/` y `outbox/`). Consulta las secciones por patrón de la guía para los trade-offs que ilustra cada ejemplo.
