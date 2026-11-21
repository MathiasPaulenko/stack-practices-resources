# Metrics Collection: Prometheus, StatsD & OpenTelemetry

Companion repository for the [Metrics Collection](https://stackpractices.com/recipes/metrics-collection/) recipe on StackPractices.

## Files

- `main.go` — Go HTTP middleware exposing a Prometheus `/metrics` endpoint (pull)
- `statsd-client.js` — Node.js StatsD client pushing counters, gauges, and timers over UDP
- `otel_metrics.py` — Python OpenTelemetry metrics exported for Prometheus scraping
- `prometheus.yml` — scrape config for the Go (`:8080`) and OTel (`:9464`) endpoints

## Quick start

```bash
# Go pull example — exposes /metrics on :8080
go mod init metrics-example && go get github.com/prometheus/client_golang/prometheus
go run main.go

# Node StatsD push example — needs a StatsD daemon on localhost:8125
npm install node-statsd
node statsd-client.js

# Python OpenTelemetry example — exposes /metrics on :9464
pip install opentelemetry-sdk opentelemetry-exporter-prometheus
python otel_metrics.py

# Point Prometheus at both endpoints
prometheus --config.file=prometheus.yml
```

Open `http://localhost:9090/targets` to confirm both jobs are `UP`, then query `http_request_duration_seconds` and `orders.created` in the expression browser.
