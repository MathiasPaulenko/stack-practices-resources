# Distributed Tracing Pattern — Companion Files

Runnable artifacts for the [Distributed Tracing pattern](https://stackpractices.com/patterns/distributed-tracing-pattern/) on StackPractices.

## Files

| File | What it shows |
|------|---------------|
| `otel_setup.py` | Shared tracer provider: resource identity, OTLP export, `ParentBased` + `TraceIdRatioBased` head sampling |
| `fastapi_traced_app.py` | FastAPI service doing both halves — middleware extracts `traceparent` inbound, handler injects it outbound |
| `rabbitmq_propagation.py` | RabbitMQ producer/consumer: context in message headers, extracted on consume so spans join the trace |
| `otel-collector-config.yaml` | Collector pipeline: OTLP in, `otlp/jaeger` + Zipkin + Tempo out, tail-sampling policies |

## Quick start

```bash
pip install -r requirements.txt

# Terminal 1 — a trace backend (Jaeger all-in-one accepts OTLP on 4317)
docker run -p 16686:16686 -p 4317:4317 -p 4318:4318 jaegertracing/all-in-one:latest

# Terminal 2 — FastAPI service (extract + inject)
uvicorn fastapi_traced_app:app --port 8000
curl -X POST "http://localhost:8000/orders?order_id=ord_42" \
  -H 'traceparent: 00-0af7651916cd43dd8448eb211c80319c-b7ad6b7169203331-01'

# RabbitMQ demo (needs a broker on 5672)
docker run -d -p 5672:5672 rabbitmq:3
python rabbitmq_propagation.py
```

Open `http://localhost:16686` and search the `order-service` / `orders-worker` services — the consumer span shows up as a child of the publish span in the same trace.

- Doc: https://stackpractices.com/patterns/distributed-tracing-pattern/
- Doc (ES): https://stackpractices.com/es/patterns/distributed-tracing-pattern/
