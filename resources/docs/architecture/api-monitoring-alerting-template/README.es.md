# Plantilla de Monitoreo y Alertas de API — Companion

Archivos companion listos para importar de la [Plantilla de Monitoreo y Alertas de API](https://stackpractices.com/es/docs/api-monitoring-alerting-template/): reglas de alerta Prometheus con burn rate rápido/lento, un JSON de dashboard Grafana y una plantilla de runbook rellenable.

## Archivos

| Archivo | Qué es |
|---------|--------|
| `alert-rules.yml` | Reglas Prometheus para el nivel de página (P0/P1), nivel de advertencia y burn rate de SLO — se cargan vía `rule_files` |
| `grafana-dashboard.json` | Dashboard de 6 paneles: gauge de disponibilidad, tasa de error, burn rate, rps, heatmap de latencia, timeline de errores |
| `runbook-template.md` | Runbook rellenable: condición de alerta → triaje en 60s → mitigación → verificación → post-incidente |

## Inicio rápido

```bash
# 1. Reglas de alerta — apunta prometheus.yml al archivo
#    rule_files:
#      - "alert-rules.yml"
promtool check rules alert-rules.yml   # valida antes de cargar

# 2. Dashboard — Grafana → Dashboards → New → Import → pega grafana-dashboard.json

# 3. Runbook — copia runbook-template.md por alerta, rellena los <placeholders>,
#    y pon la anotación runbook en alert-rules.yml apuntando a su URL
```

## Adapta a tus métricas

Las reglas asumen instrumentación estándar: contador `http_requests_total{status}` e histograma `http_request_duration_seconds_bucket` (el collector de OpenTelemetry, ingress-nginx y la mayoría de middlewares HTTP emiten estas métricas). Si tus labels difieren — p. ej. `code` en lugar de `status` — haz buscar-reemplazar tanto en las reglas como en el dashboard antes de importar.

Calibra los umbrales con la sección "Elegir los Umbrales" del doc: mide la base durante 2-4 semanas, pon los umbrales de página en ~2x la base y las advertencias en ~1.3x.

## Referencias

- Doc: https://stackpractices.com/es/docs/api-monitoring-alerting-template/
- Google SRE — Monitoring Distributed Systems: https://sre.google/sre-book/monitoring-distributed-systems/
- Google SRE Workbook — Alerting on SLOs: https://sre.google/workbook/alerting-on-slos/
- Prometheus alerting rules: https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/
