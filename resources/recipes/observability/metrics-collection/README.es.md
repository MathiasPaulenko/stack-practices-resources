# Recolección de métricas: Prometheus, StatsD y OpenTelemetry

Repositorio complementario de la receta [Recolección de métricas](https://stackpractices.com/es/recipes/metrics-collection/) en StackPractices.

## Archivos

- `main.go` — middleware HTTP en Go que expone un endpoint `/metrics` para Prometheus (pull)
- `statsd-client.js` — cliente StatsD en Node.js que envía contadores, gauges y timers por UDP
- `otel_metrics.py` — métricas de OpenTelemetry en Python expuestas para scrape de Prometheus
- `prometheus.yml` — configuración de scrape para los endpoints de Go (`:8080`) y OTel (`:9464`)

## Inicio rápido

```bash
# Ejemplo Go con pull — expone /metrics en :8080
go mod init metrics-example && go get github.com/prometheus/client_golang/prometheus
go run main.go

# Ejemplo Node con push a StatsD — requiere un demonio StatsD en localhost:8125
npm install node-statsd
node statsd-client.js

# Ejemplo Python con OpenTelemetry — expone /metrics en :9464
pip install opentelemetry-sdk opentelemetry-exporter-prometheus
python otel_metrics.py

# Apunta Prometheus a ambos endpoints
prometheus --config.file=prometheus.yml
```

Abre `http://localhost:9090/targets` para confirmar que ambos jobs están `UP` y consulta `http_request_duration_seconds` y `orders.created` en el explorador de expresiones.
