# Exporter de Métricas Prometheus en Python

Recursos companion para [Expón métricas de aplicación con Python y Prometheus](https://stackpractices.com/es/recipes/python-prometheus-metrics-exporter/).

## Archivos

- `src/basic_metrics.py` — Endpoint básico con Counter, Gauge e Histogram
- `src/flask_integration.py` — Integración con Flask con hooks before/after request
- `src/fastapi_integration.py` — Integración con FastAPI con middleware
- `src/custom_collector.py` — Collector personalizado para stats de base de datos
- `src/summary_metric.py` — Métrica Summary para percentiles
- `src/requirements.txt` — Dependencias de Python
- `prometheus.yml` — Configuración de scrape de Prometheus
- `docker-compose.yml` — Docker Compose con Prometheus + Grafana

## Inicio Rápido

```bash
pip install -r src/requirements.txt

# Ejecutar endpoint básico
python src/basic_metrics.py

# Abrir http://localhost:8000/metrics en un navegador
```

## Docker Compose

```bash
docker compose up -d
```

Inicia Prometheus en el puerto 9090 y Grafana en el puerto 3000.

## Tipos de Métricas

- **Counter**: Solo aumenta (requests, errores, bytes)
- **Gauge**: Aumenta y disminuye (conexiones activas, profundidad de cola)
- **Histogram**: Mete observaciones en buckets (latencia, tamaño de payload)
- **Summary**: Calcula percentiles en la app (percentiles exactos por instancia)

## Licencia

MIT
