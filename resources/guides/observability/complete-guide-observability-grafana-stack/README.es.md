# Observabilidad con el Stack de Grafana — Companion

Configs ejecutables de la [Guía Completa de Observabilidad con el Stack de Grafana](https://stackpractices.com/es/guides/complete-guide-observability-grafana-stack/).

## Archivos

- `docker-compose.yml` — stack LGTM completo en un archivo (Prometheus, Loki, Tempo, Alloy, Grafana, Alertmanager)
- `prometheus.yml` — config de scrape con wiring de alertado y archivos de reglas
- `alert_rules.yml` — reglas de tasa de error + burn rate de SLO (probar con `promtool test rules`)
- `alertmanager.yml` — enrutado warnings→Slack, críticos→PagerDuty
- `tempo.yaml` — receivers de Tempo (OTLP + Jaeger) y storage local
- `alloy/config.alloy` — Grafana Alloy: discovery de Docker + push a Loki (reemplaza al Promtail EOL)
- `grafana/provisioning/datasources/datasources.yml` — datasources con `uid` explícito + correlación `tracesToLogsV2`/`tracesToMetrics`/`derivedFields`
- `grafana/provisioning/dashboards/dashboards.yml` — provider de provisioning de dashboards
- `grafana/dashboards/red-metrics.json` — dashboard RED importable 
