# OpenTelemetry Guide — Companion Resources

Runnable examples for the [OpenTelemetry guide](https://stackpractices.com/guides/opentelemetry-guide/) on StackPractices.

## Contents

- `otel-collector-config.yaml` — production-shaped Collector pipeline: OTLP receivers (4317/4318), `batch`, `resourcedetection`, `tail_sampling` policies (errors, slow traces, 10 % baseline), and exporters for Jaeger, Prometheus remote write, and Loki via native OTLP/HTTP.
- `python-instrumented-app.py` — minimal working manual instrumentation: `TracerProvider` + `BatchSpanProcessor`, `MeterProvider` + `PeriodicExportingMetricReader`, resource attributes, and correct shutdown flushing.
- `docker-compose.yml` — local stack: OpenTelemetry Collector + Jaeger all-in-one (UI on `http://localhost:16686`).

## Quick start

```bash
docker compose up -d          # start collector + jaeger
pip install opentelemetry-sdk opentelemetry-exporter-otlp-proto-grpc
python python-instrumented-app.py
```

Open `http://localhost:16686`, pick `demo-service`, and you'll see the three spans (`/api/users`, `/api/orders`, `/fail`) with the simulated error marked.

## Notes

- `tls.insecure: true` in the Collector config is local-only. Use real TLS or a service mesh in production.
- The Loki and Mimir exporters in `otel-collector-config.yaml` assume those services exist; remove or swap them to match your stack.
- Head sampling can be tuned via `OTEL_TRACES_SAMPLER` / `OTEL_TRACES_SAMPLER_ARG` before running the app.
