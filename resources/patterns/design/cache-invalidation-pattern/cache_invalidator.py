"""Cache invalidation strategies for Redis — companion to the
Cache Invalidation Pattern resource on StackPractices.

Requires: pip install redis, plus a Redis server (or fakeredis for tests).
"""

import json
import threading

import redis

# decode_responses=True so r.get() returns str instead of bytes.
# Without it, versioned keys would end up like user:123:vb'1'.
r = redis.Redis(host="localhost", port=6379, decode_responses=True)


# ---------------------------------------------------------------------------
# Strategy 1: TTL-based expiration (cache-aside read path)
# ---------------------------------------------------------------------------

def get_user(user_id: str) -> dict:
    key = f"user:{user_id}"
    cached = r.get(key)
    if cached:
        return json.loads(cached)

    user = db.query_one("SELECT * FROM users WHERE id = %s", [user_id])
    r.setex(key, 300, json.dumps(user))  # 5-minute TTL
    return user


# ---------------------------------------------------------------------------
# Strategy 2: explicit invalidation on write
# ---------------------------------------------------------------------------

def update_user(user_id: str, name: str, email: str):
    db.execute(
        "UPDATE users SET name = %s, email = %s WHERE id = %s",
        [name, email, user_id],
    )
    # Invalidate the cache entry and any derived caches
    r.delete(f"user:{user_id}")
    r.delete(f"user:{user_id}:profile")
    r.delete("users:list")


# ---------------------------------------------------------------------------
# Strategy 3: event-driven invalidation with Redis pub/sub
# ---------------------------------------------------------------------------

class CacheInvalidator:
    """Publishes invalidation events so every instance evicts stale keys."""

    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
        self.pubsub = redis_client.pubsub()
        self.pubsub.subscribe("cache:invalidate")
        self._listener = threading.Thread(target=self._listen, daemon=True)
        self._listener.start()

    def invalidate(self, key: str):
        self.redis.delete(key)
        self.redis.publish("cache:invalidate", json.dumps({"key": key}))

    def invalidate_pattern(self, pattern: str):
        for key in self.redis.scan_iter(pattern):
            self.redis.delete(key)
        self.redis.publish("cache:invalidate", json.dumps({"pattern": pattern}))

    def _listen(self):
        for message in self.pubsub.listen():
            if message["type"] != "message":
                continue
            data = json.loads(message["data"])
            if "key" in data:
                self.redis.delete(data["key"])
            elif "pattern" in data:
                for key in self.redis.scan_iter(data["pattern"]):
                    self.redis.delete(key)


# ---------------------------------------------------------------------------
# Strategy 4: versioned keys
# ---------------------------------------------------------------------------

def get_user_version(user_id: str) -> str:
    version = r.get(f"user:{user_id}:version")
    if version is None:
        version = "1"
        r.set(f"user:{user_id}:version", version)
    return version


def get_user_versioned(user_id: str) -> dict:
    version = get_user_version(user_id)
    key = f"user:{user_id}:v{version}"

    cached = r.get(key)
    if cached:
        return json.loads(cached)

    user = db.query_one("SELECT * FROM users WHERE id = %s", [user_id])
    r.setex(key, 300, json.dumps(user))
    return user


def update_user_versioned(user_id: str, name: str, email: str):
    db.execute(
        "UPDATE users SET name = %s, email = %s WHERE id = %s",
        [name, email, user_id],
    )
    # Bump the version — the old key becomes orphaned and expires via TTL
    r.incr(f"user:{user_id}:version")


# `db` is a placeholder for your database layer (SQLAlchemy session, psycopg
# connection, Django ORM, etc.). Wire it up to whatever your app already uses.
