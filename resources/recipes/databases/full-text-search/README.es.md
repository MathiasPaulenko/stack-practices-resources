# Búsqueda de Texto Completo (PostgreSQL, Meilisearch, Elasticsearch)

Ejemplos ejecutables de búsqueda de texto completo en tres motores. Código complementario de la receta en
https://stackpractices.com/es/recipes/full-text-search/

## Archivos

| Archivo | Qué muestra |
|---|---|
| `full_text_search.py` | `tsvector` + índice GIN en PostgreSQL con SQLAlchemy 2.x (`text()` + `commit()`), búsqueda rankeada con `websearch_to_tsquery` |
| `meilisearch-search.js` | Settings del índice, ingesta con espera de task, búsqueda con tolerancia a errores, facetado + filtros |
| `ArticleSearch.java` | Java API Client tipado de Elasticsearch 8 (`RestHighLevelClient` se eliminó en ES 8) |
| `docker-compose.yml` | PostgreSQL 16 + Meilisearch para correr local |

## Ejecutar

```bash
docker compose up -d            # postgres + meilisearch

# Python — pip install sqlalchemy psycopg2-binary
python full_text_search.py

# JavaScript — npm install meilisearch
node meilisearch-search.js

# Java — requiere Elasticsearch 8 en :9200 y la dependencia elasticsearch-java
javac -cp "elasticsearch-java.jar;jackson-databind.jar;rest-client.jar" ArticleSearch.java
java -cp ".;elasticsearch-java.jar;jackson-databind.jar;rest-client.jar" ArticleSearch
```

El ejemplo de Python muestra por qué `websearch_to_tsquery` es el punto de entrada correcto para input
crudo del usuario: `to_tsquery` explota con comillas desbalanceadas, `plainto_tsquery` no puede expresar
frases, y `websearch_to_tsquery` acepta la sintaxis de buscador sin lanzar errores.
