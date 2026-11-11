"""Sync a PostgreSQL products table into Elasticsearch 8.

Two modes:
  - sync_product_to_es(id): upsert one document (call it from your write path
    or a queue consumer)
  - bulk_sync(): full reindex, meant for maintenance windows or bootstrapping
    a new index behind an alias

Requires:
    pip install elasticsearch psycopg2-binary

Version notes:
    - fetchone() returns a dict only with cursor_factory=RealDictCursor;
      without it rows are tuples and product["id"] raises TypeError.
    - elasticsearch-py 8 removed the body= parameter: use document= on
      index() and keyword args (query=, aggs=) on search().
"""

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import psycopg2
from psycopg2.extras import RealDictCursor

ES_URL = "http://localhost:9200"
DB_DSN = "dbname=shop"
INDEX = "products"

es = Elasticsearch(ES_URL)


def sync_product_to_es(product_id: int) -> None:
    """Upsert a single product document; delete it if the row is gone."""
    with psycopg2.connect(DB_DSN, cursor_factory=RealDictCursor) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
            product = cursor.fetchone()

    if product is None:
        es.delete(index=INDEX, id=product_id, ignore=[404])
        return

    es.index(
        index=INDEX,
        id=product["id"],
        document={
            "name": product["name"],
            "description": product["description"],
            "category": product["category"],
            "price": float(product["price"]) if product["price"] is not None else None,
            "tags": product["tags"],
            "in_stock": product["in_stock"],
        },
    )


def bulk_sync() -> None:
    """Full reindex of every product. Run during a maintenance window."""
    with psycopg2.connect(DB_DSN, cursor_factory=RealDictCursor) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM products")
            actions = (
                {
                    "_index": INDEX,
                    "_id": row["id"],
                    "_source": {
                        "name": row["name"],
                        "description": row["description"],
                        "category": row["category"],
                        "price": float(row["price"]) if row["price"] is not None else None,
                        "tags": row["tags"],
                        "in_stock": row["in_stock"],
                    },
                }
                for row in cursor
            )
            success, errors = bulk(es, actions)
            print(f"indexed={success} errors={errors}")


def search_products(query: str, category: str | None = None, max_price: float | None = None):
    """bool query: must clauses score, filter clauses only include/exclude."""
    filters = []
    if category:
        filters.append({"term": {"category": category}})
    if max_price:
        filters.append({"range": {"price": {"lte": max_price}}})

    return es.search(
        index=INDEX,
        query={
            "bool": {
                "must": {
                    "multi_match": {
                        "query": query,
                        "fields": ["name^3", "description^2", "tags"],
                        "type": "best_fields",
                        "fuzziness": "AUTO",
                    }
                },
                "filter": filters,
            }
        },
        aggs={"categories": {"terms": {"field": "category"}}},
    )


if __name__ == "__main__":
    bulk_sync()
