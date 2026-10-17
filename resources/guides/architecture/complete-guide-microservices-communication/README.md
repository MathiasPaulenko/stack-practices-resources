# Microservices Communication Patterns — Companion

Companion code for the [Complete Guide to Microservices Communication](https://stackpractices.com/guides/complete-guide-microservices-communication/).

## Overview

The code snippets from the guide as standalone files, organized by pattern. Each folder maps to a section of the guide — they are minimal, self-contained examples, not a full deployable system.

## Structure

```text
rest/
└── orders_summary.py      # FastAPI service aggregating two upstream calls (httpx + timeout)
grpc/
├── order.proto            # Protobuf contract for OrderService
└── order_client.py        # gRPC client stub call
queue/
└── order_events.py        # RabbitMQ (pika) durable queue, producer + acking consumer
pubsub/
└── order_events.js        # KafkaJS producer + consumer group subscriber
outbox/
├── OrderService.java      # Spring: business write + outbox row in one transaction
└── OutboxPublisher.java   # Scheduled relay from outbox table to Kafka
gateway/
└── kong.yaml              # Kong routes + rate-limiting and JWT plugins
mesh/
└── order-service.yaml     # Istio VirtualService 90/10 canary + DestinationRule outlierDetection
resilience/
└── payment_client.py      # httpx POST with Idempotency-Key header and timeouts
```

## Requirements

Per example:

- `rest/`, `queue/`, `resilience/`: Python 3.9+, `fastapi`, `httpx`, `pika`
- `grpc/`: `grpcio`, `grpcio-tools` — generate stubs with `python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. order.proto`
- `pubsub/`: Node.js 18+, `kafkajs`
- `outbox/`: Java 17+, Spring Boot, Spring Kafka (needs an `Order` class and an `outbox` table)
- `gateway/`: Kong Gateway (declarative config)
- `mesh/`: Kubernetes + Istio

## Usage

Run each file against its own infrastructure (a RabbitMQ container for `queue/`, a Kafka broker for `pubsub/` and `outbox/`). See the guide's per-pattern sections for the trade-offs each example illustrates.
