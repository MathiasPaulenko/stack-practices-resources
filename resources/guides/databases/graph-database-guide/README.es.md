# Bases de Datos de Grafos (Neo4j) — Archivos complementarios

Todos los ejemplos Cypher de la guía como scripts ejecutables, más un
`docker-compose.yml` que levanta Neo4j 5 con el plugin Graph Data Science: la
forma más rápida de correr todo sin instalar nada más.

Guía fuente: <https://stackpractices.com/es/guides/graph-database-guide/>

## Archivos

| Archivo | Contenido |
|---------|-----------|
| `docker-compose.yml` | Neo4j 5 + plugin GDS; UI en `localhost:7474`, Bolt en `7687` |
| `01-cypher-basics.cypher` | CREATE, recorrido `*2` de longitud variable, `shortestPath` |
| `02-recommendation-engine.cypher` | Filtrado colaborativo: quienes compraron X también compraron Y |
| `03-fraud-detection.cypher` | Detección de transferencias circulares con caminos `*3..5` |
| `04-access-control.cypher` | Verificación de pertenencia a grupos anidados con `*0..` |
| `05-hierarchies.cypher` | Recorridos de organigrama y árbol de categorías |
| `06-social-network-model.cypher` | Etiquetas, tipos de relación, índices, constraint de unicidad |
| `07-social-network-queries.cypher` | Grados de separación, recomendaciones, Louvain, habilidades complementarias |

## Ejecutar

```bash
docker compose up -d
# abre http://localhost:7474  (usuario: neo4j / contraseña: testpassword)
```

Pega cualquier `.cypher` en el editor del navegador, o pásalo por
`cypher-shell`:

```bash
cat 01-cypher-basics.cypher | docker exec -i stackpractices-neo4j \
  cypher-shell -u neo4j -p testpassword
```

## Notas

- Los recorridos de longitud variable están acotados (`*2`, `*3..5`) a propósito.
  Quitar los límites en un grafo denso es la forma clásica de reventar el heap.
- `07-social-network-queries.cypher` usa la biblioteca GDS (`gds.louvain`), ya
  habilitada en el compose vía `NEO4J_PLUGINS`.
- Las consultas asumen nodos con las propiedades de la guía (`name`, `email`,
  `location`, …). Créalos con `01-cypher-basics.cypher` o con tus propios datos
  semilla primero.
