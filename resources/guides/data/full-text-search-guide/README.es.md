# Guía de Búsqueda de Texto Completo — Código de Acompañamiento

Ejemplos ejecutables de la guía [Búsqueda de Texto Completo: Implementa Búsqueda que Funciona](https://stackpractices.com/es/guides/full-text-search-guide/).

## Archivos

| Archivo | Qué muestra |
|---------|-------------|
| `postgresql_fts.sql` | Columna `tsvector` + índice GIN, backfill ponderado con `setweight`, trigger de auto-actualización, consultas ranqueadas, resaltado con `ts_headline`, agregación de facets, autocompletado con `pg_trgm` |
| `elasticsearch_setup.json` | Mapping de índice Elasticsearch 8: analyzer personalizado (lowercase + stop words + stemmer + sinónimos), multi-campos `text`/`keyword`, completion suggester |
| `search_sync.py` | Sincronización psycopg2 → Elasticsearch 8: upsert de un documento, reindexación bulk con `helpers.bulk`, búsqueda bool con filtros y agregaciones |

## Cómo ejecutarlo

```bash
# PostgreSQL (11+): crea la tabla products, el índice, el trigger y corre consultas
psql -d yourdb -f postgresql_fts.sql

# Elasticsearch 8: crea el índice (pega el JSON en Kibana Dev Tools,
# o quita los comentarios y usa curl)
curl -X PUT localhost:9200/products -H 'Content-Type: application/json' -d @elasticsearch_setup.json

# Sincronización en Python (elasticsearch-py 8 + psycopg2)
pip install elasticsearch psycopg2-binary
python search_sync.py          # corre bulk_sync(); edita DB_DSN/ES_URL antes
```

## Notas de versión

- `fetchone()` solo devuelve un dict con `cursor_factory=RealDictCursor`; si no, las filas son tuplas.
- elasticsearch-py 8 eliminó `body=`: usa `document=` en `index()` y keyword args (`query=`, `aggs=`) en `search()`. El código escrito para v7 falla en v8.
