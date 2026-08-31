# Monitoreo de APIs con Prometheus

Repositorio companion para la receta [Monitoreo de APIs con Prometheus](https://stackpractices.com/es/recipes/prometheus-api-monitoring/) en StackPractices.

## Archivos

- `middleware.js` — Middleware de Prometheus para Node.js/Express con contador, histograma y gauge
- `middleware.go` — Middleware HTTP en Go con `prometheus/client_golang`
- `middleware.py` — Middleware en Python/Flask con `prometheus_client`
- `prometheus.yml` — Configuración de scraping de Prometheus
- `prometheus-alerts.yml` — Reglas de alerta para tasa de error y latencia alta
- `prometheus-queries.yml` — Consultas PromQL para paneles y cálculos de SLO
- `docker-compose.yml` — Stack de Prometheus + Alertmanager + Grafana

## Inicio rápido

```bash
# Iniciar el stack de monitoreo
docker-compose up -d

# Ejecutar el ejemplo en Node.js
node middleware.js

# O el ejemplo en Go
go run middleware.go

# O el ejemplo en Python
pip install flask prometheus_client
python middleware.py
```

Prometheus va a recolectar `localhost:8080/metrics` cada 15 segundos. Abrí Grafana en `localhost:3000` para visualizar las métricas.
