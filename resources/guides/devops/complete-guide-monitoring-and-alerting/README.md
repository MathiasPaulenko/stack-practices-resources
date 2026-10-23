# Monitoring & Alerting Stack — Companion Files

Runnable configuration pack for the guide
[Complete Guide to Monitoring and Alerting](https://stackpractices.com/guides/complete-guide-monitoring-and-alerting/)
([versión en español](https://stackpractices.com/es/guides/complete-guide-monitoring-and-alerting/)).

## Files

| File | Purpose |
|------|---------|
| `prometheus-values.yaml` | Helm values: persistence, retention, resources, pod scrape config |
| `metrics-instrumentation.py` | FastAPI + `prometheus_client` middleware: RED metrics, gauges, business metric |
| `dashboard-api-overview.json` | Grafana dashboard-as-code: rate, p99 latency, error rate, connections |
| `alerting-rules.yaml` | Five alert rules: error rate, p99 latency, crash loops, disk, DB pool |
| `alertmanager.yaml` | Routing tree (critical → PagerDuty, warning → Slack) + inhibit rules |
| `slo-rules.yaml` | SLI/SLO recording rules + error-budget burn-rate alert (99.9% SLO) |
| `runbook-high-error-rate.md` | Runbook template matching the `HighErrorRate` alert annotation |

## Usage

```bash
# Prometheus + AlertManager via Helm
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install prometheus prometheus-community/prometheus \
  -n monitoring --create-namespace -f prometheus-values.yaml

# Load alert rules: place alerting-rules.yaml + slo-rules.yaml in
# prometheus serverFiles rule_files / alert_rules, or a PrometheusRule CRD
# if you run kube-prometheus-stack.

# AlertManager config: mount alertmanager.yaml as the AlertManager secret,
# replacing webhook URLs and the PagerDuty routing key first.

# Dashboard: import dashboard-api-overview.json in Grafana
# (Dashboards → Import → Upload JSON) or provision it via ConfigMap.
```

All configs are starting points — adjust thresholds, retention, and receivers to your environment before production use.
