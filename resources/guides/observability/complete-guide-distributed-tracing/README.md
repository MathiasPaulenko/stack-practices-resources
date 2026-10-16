# Distributed Tracing: OpenTelemetry, Jaeger, Zipkin

Companion code for the guide [Distributed Tracing: OpenTelemetry, Jaeger, Zipkin](https://stackpractices.com/guides/complete-guide-distributed-tracing/).

## Contents

| File | What it shows |
|------|----------------|
| `instrumentation.py` | TracerProvider + BatchSpanProcessor + OTLP exporter, auto-instrumentation for Flask/requests/SQLAlchemy/Redis |
| `order_service.py` | Manual spans with parent-child nesting and error recording |
| `tracing.ts` | Node.js NodeSDK setup, auto-instrumentations, `context.with` manual span pattern |
| `kafka_propagation.py` | Trace context propagation through Kafka message headers (inject/extract) |
| `span_links.py` | Span links for batch consumers — associate traces without nesting |
| `otel-collector-config.yaml` | Production collector: memory_limiter, health-check filter, resource attrs, batching |
| `docker-compose.yml` | Jaeger all-in-one + Zipkin + OTel Collector lab |

## Quick start

```bash
# Spin up Jaeger, Zipkin and the collector
docker compose up -d

# Send some spans (any OTLP-compatible app pointed at localhost:14317)
# then open http://localhost:16686 and search for your service
```

## Notes

- The Python examples need `opentelemetry-sdk`, `opentelemetry-exporter-otlp`, the `opentelemetry-instrumentation-*` packages for your framework, and `kafka-python` for the producer/consumer sample.
- `tracing.ts` needs `@opentelemetry/sdk-node`, `@opentelemetry/exporter-trace-otlp-grpc` and the `instrumentation-*` packages listed in its imports.
- The Java agent approach (`-javaagent:opentelemetry-javaagent.jar`) is covered in the guide instead of a standalone file — it's configuration, not code.
