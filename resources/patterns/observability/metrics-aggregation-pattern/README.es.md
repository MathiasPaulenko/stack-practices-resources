# Metrics Aggregation — Recursos Companion

Código companion del [patrón Metrics Aggregation](https://stackpractices.com/es/patterns/metrics-aggregation-pattern/) en StackPractices.

## Archivos

| Archivo | Lenguaje | Descripción |
| --- | --- | --- |
| `prometheus_metrics.py` | Python 3.10+ | Los cuatro tipos de métrica (counter, gauge, histograma, summary) con un bucle de peticiones simulado y `/metrics` en el puerto 9090 |
| `business_metrics.py` | Python 3.10+ | Métricas de negocio con etiquetas dimensionales acotadas (categoría, método de pago, región) en el puerto 9091 |
| `fastapi_middleware.py` | Python 3.10+ | Middleware de FastAPI que registra conteo y latencia por petición |
| `otel_metrics.py` | Python 3.10+ | API de métricas de OpenTelemetry con el exporter de Prometheus en el puerto 9464 |
| `statsd_metrics.py` | Python 3.10+ | Variante push con StatsD para jobs batch y procesos de vida corta |
| `prom_client_express.js` | Node.js 20+ | Registry de prom-client, middleware de Express y endpoint `/metrics` |
| `prometheus.yml` | YAML | Configuración de scrape para los servicios del demo más descubrimiento en Kubernetes |
| `alerting_rules.yml` | YAML | Alertas de SLO: tasa de errores, latencia p95, servicio caído |
| `dashboard_queries.promql` | PromQL | Consultas listas para pegar en dashboards de Grafana |
| `test_metrics_aggregation.py` | Python + pytest | Verifica incrementos de counters, manejo de etiquetas, aritmética de gauges y buckets de histogramas |

## Inicio rápido

### Python (pytest)

```bash
pip install prometheus-client pytest
pytest test_metrics_aggregation.py
```

### Ejemplos en Python

```bash
pip install prometheus-client
python prometheus_metrics.py   # /metrics en :9090
python business_metrics.py     # /metrics en :9091

pip install fastapi uvicorn prometheus-client
uvicorn fastapi_middleware:app --port 8000

pip install opentelemetry-sdk opentelemetry-exporter-prometheus
python otel_metrics.py         # /metrics en :9464

pip install statsd
python statsd_metrics.py       # envía a StatsD en localhost:8125
```

### Node.js (prom-client)

```bash
npm install prom-client express
node prom_client_express.js    # app + /metrics en :3000
```

### Prometheus

Apunta un servidor Prometheus a `prometheus.yml` y carga `alerting_rules.yml` como archivo de reglas. Los snippets PromQL de `dashboard_queries.promql` cubren rate, porcentaje de errores, latencia p95 y métricas de negocio por categoría.
