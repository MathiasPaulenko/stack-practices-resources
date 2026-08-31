# Prometheus API Monitoring

Companion repository for the [Prometheus API Monitoring](https://stackpractices.com/recipes/prometheus-api-monitoring/) recipe on StackPractices.

## Files

- `middleware.js` — Node.js/Express Prometheus middleware with counter, histogram, and gauge
- `middleware.go` — Go HTTP middleware with `prometheus/client_golang`
- `middleware.py` — Python/Flask middleware with `prometheus_client`
- `prometheus.yml` — Prometheus scrape configuration
- `prometheus-alerts.yml` — Alerting rules for high error rate and latency
- `prometheus-queries.yml` — PromQL queries for dashboards and SLO calculations
- `docker-compose.yml` — Prometheus + Alertmanager + Grafana stack

## Quick start

```bash
# Start the monitoring stack
docker-compose up -d

# Run the Node.js example
node middleware.js

# Or the Go example
go run middleware.go

# Or the Python example
pip install flask prometheus_client
python middleware.py
```

Prometheus will scrape `localhost:8080/metrics` every 15 seconds. Open Grafana at `localhost:3000` to visualize the metrics.
