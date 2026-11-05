"""Query caching with Redis — requires PostgreSQL + Redis running.

  pip install psycopg2-binary redis

Caches query results under a hash of (query, params) with a TTL.
Cache queries whose results can safely be stale for the TTL —
leaderboards, catalog pages, counts. Do not cache anything the user
must see fresh: inventory, payments, permissions.
"""

import hashlib
import json

import psycopg2
import redis

r = redis.Redis(host="localhost", port=6379)
db = psycopg2.connect("dbname=app user=postgres host=localhost")


def cached_query(query: str, params: tuple, ttl: int = 300):
    """Return query results from Redis, or run the query and cache them."""
    cache_key = f"q:{hashlib.md5((query + str(params)).encode()).hexdigest()}"

    cached = r.get(cache_key)
    if cached:
        return json.loads(cached)

    cur = db.cursor()
    cur.execute(query, params)
    results = cur.fetchall()
    r.setex(cache_key, ttl, json.dumps(results, default=str))
    return results


if __name__ == "__main__":
    users = cached_query(
        "SELECT id, name FROM users WHERE status = %s",
        ("active",),
        ttl=60,
    )
    print(f"{len(users)} active users (cached for 60s)")
