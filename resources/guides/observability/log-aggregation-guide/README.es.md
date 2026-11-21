# Agregación de Logs — Pipeline Fluent Bit → Loki

Ejemplo ejecutable companion de la guía
[Guía Completa de Agregación de Logs](https://stackpractices.com/es/guides/log-aggregation-guide/).

Un pipeline de logs mínimo de extremo a extremo: una app Node.js escribe
logs JSON estructurados, un agente Fluent Bit los lee y enriquece, Loki los
almacena y Grafana expone la interfaz de consulta.

## Stack

| Componente | Rol |
|------------|-----|
| `app/` | Demo Node.js que emite logs JSON estructurados (pino) |
| `fluent-bit.conf` | Agente: tail → enriquecimiento (service/environment) → envío a Loki |
| Loki | Almacén de logs (chunks indexados por labels) |
| Grafana | Interfaz de consulta con LogQL |

## Ejecutar

```bash
docker compose up -d --build
docker compose logs -f fluent-bit   # observar el shipper
```

Abre Grafana en http://localhost:3000, añade Loki como data source
(`http://loki:3100`) y consulta en Explore:

```logql
{service="demo-service"} |= "request_handled"
sum(rate({service="demo-service"} |= "error" [1m]))
{service="demo-service"} |= "request_handled" | json | duration_ms > 400
```

## Qué demuestra

- Logging JSON estructurado desde la app (paso 1 de la guía)
- Envío agente-por-nodo con input `tail` y enriquecimiento de registros (paso 2)
- Indexación por labels en Loki y consultas LogQL (paso 4)
- Input tail con buffer en disco (`DB`) que sobrevive reinicios
