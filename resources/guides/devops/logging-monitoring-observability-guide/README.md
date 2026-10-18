# Observability Lab — Logging, Metrics, Tracing, Alerting

Runnable companion to the [Logging, Monitoring & Observability Guide](https://stackpractices.com/guides/logging-monitoring-observability-guide/) on StackPractices.

A local lab that wires an instrumented app to the full observability stack: OpenTelemetry Collector → Jaeger (traces), Prometheus (metrics), Loki (logs), Grafana (dashboards).

## Files

| File | Description |
|------|-------------|
| `payment-service.js` | Node.js service instrumented with `@opentelemetry/api`: a span per payment plus `payments.total` / `payments.errors` counters via `getMeter().createCounter()`. |
| `logging_setup.py` | structlog configuration emitting one JSON object per line, with a `bind_trace_context()` helper to stamp `trace_id`/`span_id` on every log. |
| `otel-collector-config.yaml` | Collector pipeline: OTLP receiver → batch processor → Jaeger, Prometheus and Loki exporters. |
| `prometheus-alerts.yaml` | Symptom-based alerting rules plus fast/slow SLO burn-rate alerts. |
| `prometheus.yml` | Scrape config pulling metrics from the collector's `:8889` exporter. |
| `docker-compose.yml` | Brings up the whole stack locally. |

## Run the lab

```bash
docker compose up -d
```

- Jaeger UI: http://localhost:16686 — search by `traceId` to see the full request tree
- Prometheus: http://localhost:9090 — alerts under Alerts tab, metrics under Graph
- Grafana: http://localhost:3000 (admin/admin) — add Jaeger, Prometheus and Loki as data sources

Point your app's OTLP exporter at `http://localhost:4317` (gRPC) and emit traffic — traces, metrics and logs will fan out to the three backends through the collector.

## Key idea

`trace_id` is the correlation key: it lives in the span, the log line, and (via exemplars or labels where cardinality allows) the metrics. One ID jumps you from alert → trace → logs.
