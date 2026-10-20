# Metrics and Dashboards Guide — Companion Resources

Runnable artifacts for the [Metrics and Dashboards guide](https://stackpractices.com/guides/metrics-and-dashboards-guide/) on StackPractices.

## Contents

| File | What it is |
|------|------------|
| `prometheus.yml` | Scrape configuration with Kubernetes service discovery and label-drop for high-cardinality labels |
| `recording-rules.yml` | Precomputed SLI series (request rate, error ratio, latency p95) for fast dashboards |
| `alert-rules.yml` | Symptom-based alert rules plus multi-window burn-rate alerts for a 99.9% SLO |
| `alertmanager.yml` | Routing by severity, grouping, and inhibition rules to silence cascading alerts |
| `dashboard-golden-signals.json` | Grafana dashboard: golden signals + saturation + business KPI panels |
| `instrument-app.py` | Minimal Flask app exposing Prometheus metrics on a dedicated port |

## Usage

```bash
# Validate the Prometheus config
promtool check config prometheus.yml

# Validate the rule files
promtool check rules recording-rules.yml alert-rules.yml

# Run the instrumented app (needs prometheus-client + flask)
pip install prometheus-client flask
python instrument-app.py
# Metrics at http://localhost:8000/metrics
```

Import `dashboard-golden-signals.json` into Grafana via **Dashboards → Import → Upload JSON file**. Point the `service` template variable at your service label.

## Related

- [Metrics and Dashboards Guide (EN)](https://stackpractices.com/guides/metrics-and-dashboards-guide/)
- [Guía de Métricas y Dashboards (ES)](https://stackpractices.com/es/guides/metrics-and-dashboards-guide/)
- [StackPractices resources index](https://mathiaspaulenko.github.io/stack-practices-resources/)
