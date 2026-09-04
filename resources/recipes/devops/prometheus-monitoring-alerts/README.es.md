# Prometheus Monitoring & Alerting — Companion

Ejemplos ejecutables para la receta de StackPractices
[Métricas y Alertas con Prometheus](https://stackpractices.com/es/recipes/prometheus-monitoring-alerts/).

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `metrics_server.ts` | Middleware de Express (Node.js) que expone `/metrics` con prom-client |
| `prometheus.yml` | Configuración de scraping de Prometheus |
| `alerts.yml` | Reglas de alertas (HighErrorRate, SlowRequests) |
| `records.yml` | Recording rules para queries precomputadas |
| `alertmanager.yml` | Enrutamiento de Alertmanager a email, Slack, PagerDuty |
| `custom_exporter.py` | Exporter personalizado en Python con prometheus_client |

## Inicio rápido

### Servidor de métricas Node.js

```bash
npm install prom-client express
npx tsx metrics_server.ts
# Métricas disponibles en http://localhost:3000/metrics
```

### Exporter personalizado Python

```bash
pip install prometheus-client
python custom_exporter.py
# Métricas disponibles en http://localhost:9090/metrics
```

### Prometheus + Alertmanager

```bash
prometheus --config.file=prometheus.yml --storage.tsdb.path=/tmp/prometheus
alertmanager --config.file=alertmanager.yml
```

Apuntá Prometheus a tus endpoints de métricas y las reglas de alertas van a dispararse
según los umbrales configurados.

## Fuente

- [Receta (EN)](https://stackpractices.com/recipes/prometheus-monitoring-alerts/)
- [Receta (ES)](https://stackpractices.com/es/recipes/prometheus-monitoring-alerts/)
