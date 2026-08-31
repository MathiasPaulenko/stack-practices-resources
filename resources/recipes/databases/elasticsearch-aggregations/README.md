# How to Use Elasticsearch Aggregations (With Examples)

Runnable companion project for the StackPractices recipe.

## What it contains

- `python/products_aggregations.py` — seed sample products and run `terms`, `stats`, and `percentiles` aggregations with the official Python client.
- `javascript/search_client.mjs` — faceted search, revenue histogram, and composite pagination with the official JavaScript client.
- `queries/` — copy-paste JSON queries for the Elasticsearch REST API.
- `docker-compose.yml` — a single-node Elasticsearch 8.15.0 container.
- `requirements.txt` — Python dependencies.
- `package.json` — JavaScript dependencies.

## Run locally with Docker

```bash
docker compose up -d
curl -f http://localhost:9200/_cluster/health
```

## Run the Python example

```bash
python -m venv .venv
# on Windows: .venv\Scripts\activate
# on Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
python python/products_aggregations.py
```

## Run the JavaScript example

```bash
npm install
node javascript/search_client.mjs laptop
```

## Run the JSON queries

```bash
# Create the index mapping
curl -X PUT http://localhost:9200/products -H "Content-Type: application/json" -d @queries/setup_index.json

# Term facets
curl -X GET http://localhost:9200/products/_search -H "Content-Type: application/json" -d @queries/terms_facet.json
```

> This is a local learning setup. For production, use a proper cluster with
> security enabled and dedicated master/data nodes.

## Files

| File | Purpose |
| --- | --- |
| `python/products_aggregations.py` | Python client examples with sample data |
| `javascript/search_client.mjs` | JavaScript client examples |
| `queries/setup_index.json` | Index mapping with `keyword` subfields |
| `queries/terms_facet.json` | Faceted search with `terms` |
| `queries/date_histogram_revenue.json` | Time-series revenue aggregation |
| `queries/composite_pagination.json` | Deep pagination with `composite` |
| `docker-compose.yml` | Local single-node Elasticsearch |
| `requirements.txt` | Python dependencies |
| `package.json` | JavaScript dependencies |

## Links

- Recipe: <https://stackpractices.com/recipes/elasticsearch-aggregations/>
- Elasticsearch docs: <https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations.html>
