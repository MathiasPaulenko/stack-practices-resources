# Metrics Aggregation — Companion Resources

Companion code for the [Metrics Aggregation pattern](https://stackpractices.com/patterns/metrics-aggregation-pattern/) on StackPractices.

## Files

| File | Language | Description |
| --- | --- | --- |
| `prometheus_metrics.py` | Python 3.10+ | All four metric types (counter, gauge, histogram, summary) with a simulated request loop and `/metrics` on port 9090 |
| `business_metrics.py` | Python 3.10+ | Business metrics with bounded dimensional tags (category, payment method, region) on port 9091 |
| `fastapi_middleware.py` | Python 3.10+ | FastAPI middleware that records count and latency for every request |
| `otel_metrics.py` | Python 3.10+ | OpenTelemetry metrics API with the Prometheus exporter on port 9464 |
| `statsd_metrics.py` | Python 3.10+ | Push-based variant with StatsD for batch jobs and short-lived processes |
| `prom_client_express.js` | Node.js 20+ | prom-client registry, Express middleware and `/metrics` endpoint |
| `prometheus.yml` | YAML | Scrape configuration for the demo services plus Kubernetes service discovery |
| `alerting_rules.yml` | YAML | SLO alerts: error rate, p95 latency, service down |
| `dashboard_queries.promql` | PromQL | Ready-to-paste queries for Grafana dashboards |
| `test_metrics_aggregation.py` | Python + pytest | Verifies counter increments, label handling, gauge math and histogram buckets |

## Quick start

### Python (pytest)

```bash
pip install prometheus-client pytest
pytest test_metrics_aggregation.py
```

### Python examples

```bash
pip install prometheus-client
python prometheus_metrics.py   # /metrics on :9090
python business_metrics.py     # /metrics on :9091

pip install fastapi uvicorn prometheus-client
uvicorn fastapi_middleware:app --port 8000

pip install opentelemetry-sdk opentelemetry-exporter-prometheus
python otel_metrics.py         # /metrics on :9464

pip install statsd
python statsd_metrics.py       # pushes to StatsD on localhost:8125
```

### Node.js (prom-client)

```bash
npm install prom-client express
node prom_client_express.js    # app + /metrics on :3000
```

### Prometheus

Point a Prometheus server at `prometheus.yml` and load `alerting_rules.yml` as a rule file. The PromQL snippets in `dashboard_queries.promql` cover rate, error percentage, p95 latency and per-category business metrics.
