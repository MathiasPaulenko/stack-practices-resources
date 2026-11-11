# Full-Text Search Guide — Companion Code

Runnable examples for the guide [Full-Text Search: Implement Search That Actually Works](https://stackpractices.com/guides/full-text-search-guide/).

## Files

| File | What it shows |
|------|---------------|
| `postgresql_fts.sql` | `tsvector` column + GIN index, weighted `setweight` backfill, auto-update trigger, ranked queries, `ts_headline` highlighting, facet aggregation, `pg_trgm` autocomplete |
| `elasticsearch_setup.json` | Elasticsearch 8 index mapping: custom analyzer (lowercase + stop words + stemmer + synonyms), `text`/`keyword` multi-fields, completion suggester |
| `search_sync.py` | psycopg2 → Elasticsearch 8 sync: single-document upsert, bulk reindex with `helpers.bulk`, bool search with filters and aggregations |

## Run it

```bash
# PostgreSQL (11+): creates the products table, index, trigger, then runs queries
psql -d yourdb -f postgresql_fts.sql

# Elasticsearch 8: create the index (paste the JSON into Kibana Dev Tools,
# or strip comments and curl it)
curl -X PUT localhost:9200/products -H 'Content-Type: application/json' -d @elasticsearch_setup.json

# Python sync (elasticsearch-py 8 + psycopg2)
pip install elasticsearch psycopg2-binary
python search_sync.py          # runs bulk_sync(); edit DB_DSN/ES_URL first
```

## Version notes

- `fetchone()` only returns a dict with `cursor_factory=RealDictCursor`; otherwise rows are tuples.
- elasticsearch-py 8 removed `body=`: use `document=` on `index()` and keyword args (`query=`, `aggs=`) on `search()`. Code written for v7 fails on v8.
