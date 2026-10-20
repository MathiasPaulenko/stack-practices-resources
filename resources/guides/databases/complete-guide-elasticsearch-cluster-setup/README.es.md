# Cluster de Elasticsearch — Configuraciones de Producción

Recursos companion de la guía [Guía Completa para Configurar un Cluster de Elasticsearch](https://stackpractices.com/es/guides/complete-guide-elasticsearch-cluster-setup/).

## Archivos

| Archivo | Qué es |
| --- | --- |
| `elasticsearch.yml` | Configuración comentada de producción para 3 nodos (master+data, seguridad, memory lock, disk watermarks). Cambia `node.name` por host; elimina `cluster.initial_master_nodes` tras el primer bootstrap. |
| `docker-compose.yml` | Cluster de prueba de 3 nodos con ES 8.15 en red privada — seguridad activada, contraseña de `elastic` por variable de entorno, HTTP en 9200 para `curl` local. No es una receta de producción. |
| `ilm-policy.json` | Ciclo de vida hot/warm/cold/delete para índices `logs-*` (rollover 7d/50GB → shrink+forcemerge a 30d → nodos cold a 90d → delete a 365d). |
| `index-template.json` | Settings + mappings + conexión ILM para `logs-*` — donde viven los defaults de índice en ES 8. |

## Uso

```bash
# Cluster de prueba local
docker compose up -d
curl -u elastic:$ELASTIC_PASSWORD http://localhost:9200

# Aplicar template y política (el orden importa: primero la política)
curl -u elastic:$ELASTIC_PASSWORD -XPUT http://localhost:9200/_ilm/policy/logs-policy \
  -H 'Content-Type: application/json' -d @ilm-policy.json
curl -u elastic:$ELASTIC_PASSWORD -XPUT http://localhost:9200/_index_template/logs \
  -H 'Content-Type: application/json' -d @index-template.json
```

## Trampas

- `cluster.initial_master_nodes` es **solo bootstrap** — quítalo cuando el cluster se forme.
- `bootstrap.memory_lock: true` falla sin `vm.max_map_count >= 262144` y un límite de fd adecuado en el host.
- La acción `freeze` de ILM está deprecated en ES 8 — la fase cold usa `allocate` o searchable snapshots.
- Los defaults de índice (`index.*`) no existen como settings de nodo en ES 8; viven en el index template.
