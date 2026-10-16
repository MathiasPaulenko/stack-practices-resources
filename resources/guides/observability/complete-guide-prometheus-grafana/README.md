# Prometheus and Grafana: Metrics, Dashboards, Alerting

Companion code for the guide [Prometheus and Grafana: Metrics, Dashboards, Alerting](https://stackpractices.com/guides/complete-guide-prometheus-grafana/).

## Contents

| File | What it shows |
|------|----------------|
| `docker-compose.yml` | Full stack: Prometheus + Grafana + Alertmanager + node-exporter |
| `prometheus.yml` | Scrape config: static targets, rule files, Alertmanager endpoint |
| `alertmanager.yml` | Routing tree: critical → PagerDuty, default → Slack |
| `alerting_rules.yml` | Five alerting rules plus two recording rules |
| `grafana/provisioning/datasources/datasource.yml` | Prometheus data source provisioning (required for dashboards to render) |
| `grafana/provisioning/dashboards/dashboards.yml` | File-based dashboard provider |
| `grafana/dashboards/order-service.json` | Example dashboard: request rate, error rate stat, P99/P95 latency |
| `metrics.py` | Python `prometheus_client` instrumentation + Flask `/metrics` |
| `metrics.ts` | Node.js `prom-client` instrumentation + Express `/metrics` |
| `MetricsConfig.java` | Micrometer `PrometheusMeterRegistry`, JVM binders, Spring `/metrics` |

## Quick start

```bash
# Set the Grafana admin password first
export GRAFANA_ADMIN_PASSWORD=changeme

docker compose up -d

# Prometheus targets: http://localhost:9090/targets
# Grafana:           http://localhost:3000
# Alertmanager:      http://localhost:9093
```

## Notes

- `metrics.py` needs `prometheus-client` and `flask`; `metrics.ts` needs `prom-client` and `express`; the Java example needs `micrometer-registry-prometheus` and Spring.
- The `order-service` and `api-gateway` scrape jobs expect your apps running on those hostnames — edit `prometheus.yml` or add the services to the compose file.
- Slack and PagerDuty receivers in `alertmanager.yml` contain placeholder URLs/keys — replace them before pointing real alerts at them.
- Validate rule files with `promtool check rules alerting_rules.yml` before deploying.
