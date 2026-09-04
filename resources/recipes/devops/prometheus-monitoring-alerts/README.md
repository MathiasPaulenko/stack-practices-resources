# Prometheus Monitoring & Alerting — Companion

Runnable examples for the StackPractices recipe
[Metrics Collection and Alerting with Prometheus](https://stackpractices.com/recipes/prometheus-monitoring-alerts/).

## Files

| File | Description |
|------|-------------|
| `metrics_server.ts` | Node.js Express middleware exposing `/metrics` with prom-client |
| `prometheus.yml` | Prometheus scrape configuration |
| `alerts.yml` | Alerting rules (HighErrorRate, SlowRequests) |
| `records.yml` | Recording rules for precomputed queries |
| `alertmanager.yml` | Alertmanager routing to email, Slack, PagerDuty |
| `custom_exporter.py` | Custom Python exporter using prometheus_client |

## Quick start

### Node.js metrics server

```bash
npm install prom-client express
npx tsx metrics_server.ts
# Metrics available at http://localhost:3000/metrics
```

### Python custom exporter

```bash
pip install prometheus-client
python custom_exporter.py
# Metrics available at http://localhost:9090/metrics
```

### Prometheus + Alertmanager

```bash
prometheus --config.file=prometheus.yml --storage.tsdb.path=/tmp/prometheus
alertmanager --config.file=alertmanager.yml
```

Point Prometheus at your metrics endpoints and the alerting rules will fire based on the
configured thresholds.

## Source

- [Recipe (EN)](https://stackpractices.com/recipes/prometheus-monitoring-alerts/)
- [Recipe (ES)](https://stackpractices.com/es/recipes/prometheus-monitoring-alerts/)
