# Python Prometheus Metrics Exporter

Companion resources for [Expose Custom Application Metrics with Python and Prometheus](https://stackpractices.com/recipes/python-prometheus-metrics-exporter/).

## Files

- `src/basic_metrics.py` — Basic metrics endpoint with Counter, Gauge, and Histogram
- `src/flask_integration.py` — Flask integration with before/after request hooks
- `src/fastapi_integration.py` — FastAPI integration with middleware
- `src/custom_collector.py` — Custom collector for external database stats
- `src/summary_metric.py` — Summary metric for percentile tracking
- `src/requirements.txt` — Python dependencies
- `prometheus.yml` — Prometheus scrape configuration
- `docker-compose.yml` — Docker Compose with Prometheus + Grafana

## Quick Start

```bash
pip install -r src/requirements.txt

# Run basic metrics endpoint
python src/basic_metrics.py

# Open http://localhost:8000/metrics in a browser
```

## Docker Compose

```bash
docker compose up -d
```

This starts Prometheus on port 9090 and Grafana on port 3000.

## Metric Types

- **Counter**: Only increases (requests, errors, bytes)
- **Gauge**: Increases and decreases (active connections, queue depth)
- **Histogram**: Bins observations into buckets (latency, payload size)
- **Summary**: Computes percentiles in-app (exact per-instance percentiles)

## License

MIT
