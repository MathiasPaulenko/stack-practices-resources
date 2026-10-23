# Stack de Monitoreo y Alertas — Archivos del Companion

Pack de configuración ejecutable de la guía
[Guía Completa de Monitoreo y Alertas](https://stackpractices.com/es/guides/complete-guide-monitoring-and-alerting/)
([English version](https://stackpractices.com/guides/complete-guide-monitoring-and-alerting/)).

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `prometheus-values.yaml` | Valores Helm: persistencia, retención, recursos, scrape de pods |
| `metrics-instrumentation.py` | Middleware FastAPI + `prometheus_client`: métricas RED, gauges, métrica de negocio |
| `dashboard-api-overview.json` | Dashboard de Grafana como código: rate, latencia p99, tasa de error, conexiones |
| `alerting-rules.yaml` | Cinco reglas de alerta: tasa de error, latencia p99, crash loops, disco, pool de BD |
| `alertmanager.yaml` | Árbol de routing (critical → PagerDuty, warning → Slack) + inhibit rules |
| `slo-rules.yaml` | Recording rules de SLI/SLO + alerta de burn rate del error budget (SLO 99,9%) |
| `runbook-high-error-rate.md` | Plantilla de runbook enlazada desde la anotación de `HighErrorRate` |

## Uso

```bash
# Prometheus + AlertManager con Helm
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install prometheus prometheus-community/prometheus \
  -n monitoring --create-namespace -f prometheus-values.yaml

# Reglas de alerta: copia alerting-rules.yaml + slo-rules.yaml a
# serverFiles de Prometheus (rule_files / alert_rules) o a un CRD
# PrometheusRule si usas kube-prometheus-stack.

# AlertManager: monta alertmanager.yaml como el secret del AlertManager,
# sustituyendo primero los webhooks y la routing key de PagerDuty.

# Dashboard: importa dashboard-api-overview.json en Grafana
# (Dashboards → Import → Upload JSON) o provisiona por ConfigMap.
```

Todas las configuraciones son puntos de partida — ajusta umbrales, retención y receivers a tu entorno antes de producción.
