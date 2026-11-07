# Correlation ID Pattern — Companion Files

Runnable artifacts for the [Correlation ID pattern](https://stackpractices.com/patterns/correlation-id-pattern/) on StackPractices.

## Files

| File | What it shows |
|------|---------------|
| `correlation_middleware.py` | FastAPI middleware: generate-or-reuse at the edge, `contextvars` storage, structured JSON logging filter |
| `correlation-middleware.mjs` | Node/Express middleware with `AsyncLocalStorage` — ID survives `await` without threading `req` through helpers |
| `rabbitmq_correlation.py` | RabbitMQ publisher + consumer: ID in message headers AND body metadata, extraction with fallback |
| `CorrelationIdFilter.java` | Spring Boot `OncePerRequestFilter` + MDC + `RestTemplate` interceptor for downstream propagation |

## Quick start

```bash
# FastAPI
pip install fastapi uvicorn
uvicorn correlation_middleware:app --reload
curl -i http://localhost:8000/orders -H "X-Correlation-ID: demo-123"

# Node (no deps needed for the demo server)
node correlation-middleware.mjs
curl -i http://localhost:3000/orders -H "x-correlation-id: demo-123"

# RabbitMQ (needs a local broker)
pip install pika
python rabbitmq_correlation.py
```

The demo services echo the correlation ID back in the response headers and print it in every log line — send your own `X-Correlation-ID` and watch it survive, or omit it and see a UUID generated.

- Doc: https://stackpractices.com/patterns/correlation-id-pattern/
- Doc (ES): https://stackpractices.com/es/patterns/correlation-id-pattern/
