# Prometheus y Grafana: métricas, dashboards y alertas

Código de la guía [Prometheus y Grafana: métricas, dashboards y alertas](https://stackpractices.com/es/guides/complete-guide-prometheus-grafana/).

## Contenido

| Archivo | Qué muestra |
|---------|-------------|
| `docker-compose.yml` | Stack completo: Prometheus + Grafana + Alertmanager + node-exporter |
| `prometheus.yml` | Config de scrape: targets estáticos, archivos de reglas, endpoint de Alertmanager |
| `alertmanager.yml` | Árbol de enrutado: critical → PagerDuty, default → Slack |
| `alerting_rules.yml` | Cinco reglas de alerta más dos recording rules |
| `grafana/provisioning/datasources/datasource.yml` | Aprovisionamiento del data source de Prometheus (necesario para que los dashboards rendericen) |
| `grafana/provisioning/dashboards/dashboards.yml` | Proveedor de dashboards basado en archivos |
| `grafana/dashboards/order-service.json` | Dashboard de ejemplo: request rate, stat de error rate, latencia P99/P95 |
| `metrics.py` | Instrumentación con `prometheus_client` de Python + `/metrics` en Flask |
| `metrics.ts` | Instrumentación con `prom-client` de Node.js + `/metrics` en Express |
| `MetricsConfig.java` | `PrometheusMeterRegistry` de Micrometer, binders de JVM, `/metrics` en Spring |

## Inicio rápido

```bash
# Define primero la contraseña de admin de Grafana
export GRAFANA_ADMIN_PASSWORD=cambiame

docker compose up -d

# Targets de Prometheus: http://localhost:9090/targets
# Grafana:               http://localhost:3000
# Alertmanager:          http://localhost:9093
```

## Notas

- `metrics.py` necesita `prometheus-client` y `flask`; `metrics.ts` necesita `prom-client` y `express`; el ejemplo Java necesita `micrometer-registry-prometheus` y Spring.
- Los jobs `order-service` y `api-gateway` esperan tus apps corriendo en esos hostnames — edita `prometheus.yml` o añade los servicios al compose.
- Los receptores de Slack y PagerDuty en `alertmanager.yml` llevan URLs/claves de ejemplo — reemplázalas antes de apuntar alertas reales.
- Valida los archivos de reglas con `promtool check rules alerting_rules.yml` antes de desplegar.
