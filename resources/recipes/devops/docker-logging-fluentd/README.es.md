# Logging en Docker con Fluentd — Archivos complementarios

Archivos ejecutables de la receta de StackPractices [Centraliza Logs de Contenedores con Fluentd y Docker](https://stackpractices.com/es/recipes/docker-logging-fluentd/).

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `fluentd.conf` | Input forward + filtros record_transformer/parser + fan-out con `@type copy` a Elasticsearch y stdout |
| `fluentd-sidecar.conf` | Source `tail` para apps que escriben a archivos de log |
| `fluentd-s3.conf` | Variante con output a S3 para archivo en frío |
| `docker-compose.yml` | Stack completo: Fluentd + Elasticsearch + Kibana + app demo con el driver fluentd |
| `docker-compose.sidecar.yml` | Variante sidecar: volumen compartido + tail de archivo |
| `Dockerfile` | Imagen mínima de la app demo en Node |
| `server.js` | App Node que emite logs JSON estructurados a stdout |
| `app.py` | Variante en Python con `JsonFormatter` |
| `verify-pipeline.sh` | Checks de punta a punta: Fluentd arriba, evento de prueba con fluent-cat, índice en ES, documentos de muestra |

## Inicio rápido

```bash
docker compose up -d
docker logs -f api          # la app emite logs JSON
curl localhost:9200/_cat/indices?v
./verify-pipeline.sh
```

Después abre Kibana en `http://localhost:5601`, crea un data view sobre `docker-logs-*` y consulta `service:api AND level:error` en Discover.

La variante sidecar se levanta con `docker compose -f docker-compose.sidecar.yml up -d` — hace tail de `/var/log/app/app.log` a través del volumen compartido `api-logs` en lugar de usar el driver de logging.
