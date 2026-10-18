# Laboratorio de Observabilidad — Logging, Métricas, Tracing, Alertas

Companion ejecutable de la [Guía de Logging, Monitoreo y Observabilidad](https://stackpractices.com/es/guides/logging-monitoring-observability-guide/) en StackPractices.

Un laboratorio local que conecta una app instrumentada con el stack completo de observabilidad: OpenTelemetry Collector → Jaeger (traces), Prometheus (métricas), Loki (logs), Grafana (dashboards).

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `payment-service.js` | Servicio Node.js instrumentado con `@opentelemetry/api`: un span por pago y los counters `payments.total` / `payments.errors` vía `getMeter().createCounter()`. |
| `logging_setup.py` | Configuración de structlog que emite un objeto JSON por línea, con el helper `bind_trace_context()` para estampar `trace_id`/`span_id` en cada log. |
| `otel-collector-config.yaml` | Pipeline del collector: receptor OTLP → procesador batch → exportadores Jaeger, Prometheus y Loki. |
| `prometheus-alerts.yaml` | Reglas de alerta basadas en síntomas más alertas de burn rate de SLO (rápida y lenta). |
| `prometheus.yml` | Config de scrape que toma métricas del exportador `:8889` del collector. |
| `docker-compose.yml` | Levanta todo el stack en local. |

## Ejecutar el laboratorio

```bash
docker compose up -d
```

- Jaeger UI: http://localhost:16686 — busca por `traceId` para ver el árbol completo de la petición
- Prometheus: http://localhost:9090 — alertas en la pestaña Alerts, métricas en Graph
- Grafana: http://localhost:3000 (admin/admin) — agrega Jaeger, Prometheus y Loki como data sources

Apunta el exportador OTLP de tu app a `http://localhost:4317` (gRPC) y genera tráfico — traces, métricas y logs se distribuirán a los tres backends a través del collector.

## Idea clave

`trace_id` es la clave de correlación: vive en el span, en la línea de log y (vía exemplars o labels donde la cardinalidad lo permite) en las métricas. Un solo ID te lleva de alerta → trace → logs.
