# Full-Text Search (PostgreSQL, Meilisearch, Elasticsearch)

Runnable full-text search examples across three engines. Companion code for the recipe at
https://stackpractices.com/recipes/full-text-search/

## Files

| File | What it shows |
|---|---|
| `full_text_search.py` | PostgreSQL `tsvector` + GIN index with SQLAlchemy 2.x (`text()` + `commit()`), ranked search via `websearch_to_tsquery` |
| `meilisearch-search.js` | Index settings, document ingest with task wait, typo-tolerant search, faceting + filters |
| `ArticleSearch.java` | Elasticsearch 8 typed Java API Client (`RestHighLevelClient` was removed in ES 8) |
| `docker-compose.yml` | PostgreSQL 16 + Meilisearch for local runs |

## Run

```bash
docker compose up -d            # postgres + meilisearch

# Python — pip install sqlalchemy psycopg2-binary
python full_text_search.py

# JavaScript — npm install meilisearch
node meilisearch-search.js

# Java — needs Elasticsearch 8 on :9200 and the elasticsearch-java dependency
javac -cp "elasticsearch-java.jar;jackson-databind.jar;rest-client.jar" ArticleSearch.java
java -cp ".;elasticsearch-java.jar;jackson-databind.jar;rest-client.jar" ArticleSearch
```

The Python example demonstrates why `websearch_to_tsquery` is the right entry point for raw user
input: `to_tsquery` throws on unbalanced quotes, `plainto_tsquery` can't express phrases, and
`websearch_to_tsquery` accepts search-box syntax without raising.
