# Dashboards de Grafana para Observabilidad con Prometheus

Recurso companion para [StackPractices](https://stackpractices.com/es/recipes/grafana-dashboards-observability/).

## Contenidos

- `provisioning/datasources/prometheus.yml` — Data source de Prometheus
- `provisioning/datasources/loki.yml` — Data source de Loki para logs
- `provisioning/dashboards/dashboards.yml` — Config del provider de dashboards
- `provisioning/dashboards/api-overview.json` — Dashboard API Service Overview
- `provisioning/alerting/alerts.yml` — Reglas de alerta de Grafana
- `terraform/grafana.tf` — Dashboard manejado con Terraform
- `recording-rules.yml` — Recording rules de Prometheus para queries caros

## Uso

1. Copiá `provisioning/` en tu directorio de provisioning de Grafana.
2. Iniciá Grafana — carga data sources, dashboards y alertas automáticamente.
3. Aplicá `terraform/grafana.tf` si preferís dashboards manejados con Terraform.
4. Cargá `recording-rules.yml` en Prometheus para métricas pre-computadas.

## Requisitos

- Grafana 10+
- Prometheus 2.40+
- Loki 2.8+ (opcional, para paneles de logs)
- Terraform 1.5+ (opcional, para dashboards IaC)
