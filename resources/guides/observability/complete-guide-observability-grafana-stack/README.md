# Observability with the Grafana Stack — Companion

Runnable configs from the [Complete Guide to Observability with the Grafana Stack](https://stackpractices.com/guides/complete-guide-observability-grafana-stack/).

## Files

- `docker-compose.yml` — full LGTM stack in one file (Prometheus, Loki, Tempo, Alloy, Grafana, Alertmanager)
- `prometheus.yml` — scrape config with alerting wiring and rule files
- `alert_rules.yml` — error-rate + SLO burn-rate alert rules (test with `promtool test rules`)
- `alertmanager.yml` — routing warnings→Slack, critical→PagerDuty
- `tempo.yaml` — Tempo receivers (OTLP + Jaeger) and local storage
- `alloy/config.alloy` — Grafana Alloy: Docker discovery + Loki push (replaces EOL Promtail)
- `grafana/provisioning/datasources/datasources.yml` — datasources with explicit `uid` + `tracesToLogsV2`/`tracesToMetrics`/`derivedFields` correlation
- `grafana/provisioning/dashboards/dashboards.yml` — dashboard provisioning provider
- `grafana/dashboards/red-metrics.json` — importable RED dashboard (uid, schemaVersion, gridPos)
- `otel-collector-config.yaml` — OTel Collector with tail sampling (errors + slow + 10%)
- `otel_tracing.py` / `otel_tracing.js` — OTel instrumentation for Flask and Node/Express

## Usage

```bash
docker compose up -d
# Grafana → http://localhost:3000  (anonymous login — dev only)
# Prometheus → http://localhost:9090 · Loki :3100 · Tempo :3200 · Alertmanager :9093
```

Set your real Slack webhook / PagerDuty key in `alertmanager.yml` and point `app:8080` in `prometheus.yml` at your instrumented service.

## Requirements

- Docker Compose v2
- A service exposing `/metrics` (or OTel) to send signals to the stack
