# Grafana Dashboards for Observability with Prometheus

Companion resource for [StackPractices](https://stackpractices.com/recipes/grafana-dashboards-observability/).

## Contents

- `provisioning/datasources/prometheus.yml` — Prometheus data source
- `provisioning/datasources/loki.yml` — Loki data source for logs
- `provisioning/dashboards/dashboards.yml` — Dashboard provider config
- `provisioning/dashboards/api-overview.json` — API Service Overview dashboard
- `provisioning/alerting/alerts.yml` — Grafana alert rules
- `terraform/grafana.tf` — Terraform-managed dashboard
- `recording-rules.yml` — Prometheus recording rules for expensive queries

## Usage

1. Copy `provisioning/` into your Grafana provisioning directory.
2. Start Grafana — it loads data sources, dashboards, and alerts automatically.
3. Apply `terraform/grafana.tf` if you prefer Terraform-managed dashboards.
4. Load `recording-rules.yml` into Prometheus for pre-computed metrics.

## Requirements

- Grafana 10+
- Prometheus 2.40+
- Loki 2.8+ (optional, for log panels)
- Terraform 1.5+ (optional, for IaC-managed dashboards)
