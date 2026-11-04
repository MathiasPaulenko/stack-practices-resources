# GraphQL Federation en Producción — Recursos complementarios

Archivos de configuración listos para producción de la guía
[GraphQL Federation en Producción](https://stackpractices.com/es/guides/complete-guide-graphql-federation-production/).

## Contenido

| Archivo | Propósito |
| --- | --- |
| `router.yaml` | Config de producción de Apollo Router: health checks, timeouts, persisted queries, límites, CSRF, propagación de cabeceras, exportación OTel |
| `supergraph.yaml` | Config de composición del supergraph para Rover en modo autoalojado |
| `docker-compose.yml` | Contenedor del router en modo gestionado (consulta Uplink) |
| `k8s/deployment.yaml` | Deployment del router con 3 réplicas y sondas en el puerto 8088 |
| `schema-ownership.yaml` | Mapa de propiedad de tipos/campos legible por máquinas |
| `src/users-subgraph.js` | Subgrafo Users con `__resolveReference` (agrúpalo en código real) |
| `ci/check-schema.sh` | Paso de CI: `rover subgraph check` antes de publicar |

## Uso

```bash
# Componer el supergraph en local
rover supergraph compose --config supergraph.yaml > supergraph.graphql

# Ejecutar el router contra el archivo compuesto
./router --supergraph supergraph.graphql --config router.yaml

# O modo gestionado (consulta Uplink)
docker compose up
```

Los health checks viven en el puerto `8088` (`/health`, `?live`, `?ready`).
Amplía `health_check.listen` a `0.0.0.0` dentro de contenedores.
