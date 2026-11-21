# Agregación de Logs — Ejemplos Ejecutables

Companion ejecutable de la [receta de agregación de logs](https://stackpractices.com/es/recipes/log-aggregation/) en StackPractices.

## Contenido

| Archivo | Qué es |
| --- | --- |
| `docker-compose.yml` | Stack Fluentd → Elasticsearch → Kibana con volumen persistente para el buffer |
| `fluent.conf` | Entrada forward, filtro de parsing JSON, salida a Elasticsearch con buffering en disco y reintentos con backoff exponencial |
| `app/logger.js` | Logger estructurado de Winston que emite líneas JSON con correlación por `traceId` |
| `app/package.json` | Proyecto Node mínimo (solo `winston`) |

## Levantar el stack

```bash
docker compose up -d
# Kibana → http://localhost:5601  |  Elasticsearch → http://localhost:9200
```

Envía un log de prueba por el protocolo forward de Fluentd:

```bash
echo '{"log":"{\"level\":\"info\",\"event\":\"test\",\"service\":\"demo\"}"}' | \
  docker exec -i $(docker ps -qf ancestor=fluent/fluentd:v1.16) fluent-cat app.demo
```

Después crea el index pattern `app-*` en Kibana para explorarlo.

## Ejecutar el logger

```bash
cd app
npm install
npm start
```

Escribe tres líneas JSON correlacionadas en stdout y en `app.log` — el formato que espera un tail de Fluent Bit o un scrape de Promtail.
