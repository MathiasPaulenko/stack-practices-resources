# Guía de Métricas y Dashboards — Recursos Companion

Artefactos ejecutables para la [Guía de Métricas y Dashboards](https://stackpractices.com/es/guides/metrics-and-dashboards-guide/) de StackPractices.

## Contenido

| Archivo | Qué es |
|---------|--------|
| `prometheus.yml` | Configuración de scrape con descubrimiento de servicios de Kubernetes y descarte de labels de alta cardinalidad |
| `recording-rules.yml` | Series SLI precomputadas (tasa de peticiones, ratio de error, latencia p95) para dashboards rápidos |
| `alert-rules.yml` | Reglas de alerta por síntomas más alertas de burn rate multi-ventana para un SLO del 99,9% |
| `alertmanager.yml` | Enrutado por severidad, agrupación y reglas de inhibición para silenciar alertas en cascada |
| `dashboard-golden-signals.json` | Dashboard de Grafana: señales doradas + saturación + paneles de KPI de negocio |
| `instrument-app.py` | App Flask mínima que expone métricas de Prometheus en un puerto dedicado |

## Uso

```bash
# Validar la configuración de Prometheus
promtool check config prometheus.yml

# Validar los archivos de reglas
promtool check rules recording-rules.yml alert-rules.yml

# Ejecutar la app instrumentada (necesita prometheus-client + flask)
pip install prometheus-client flask
python instrument-app.py
# Métricas en http://localhost:8000/metrics
```

Importa `dashboard-golden-signals.json` en Grafana desde **Dashboards → Import → Upload JSON file**. Apunta la variable `service` al label de tu servicio.

## Relacionados

- [Guía de Métricas y Dashboards (ES)](https://stackpractices.com/es/guides/metrics-and-dashboards-guide/)
- [Metrics and Dashboards Guide (EN)](https://stackpractices.com/guides/metrics-and-dashboards-guide/)
- [Índice de recursos de StackPractices](https://mathiaspaulenko.github.io/stack-practices-resources/)
