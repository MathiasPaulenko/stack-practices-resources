"""Write-behind cache with a durable dirty set in Redis.

The dirty set lives in Redis itself (not in process memory), so an
application restart does not lose the flush queue. A background thread
batches pending keys to the database every `flush_interval` seconds.

Requires: pip install redis (use fakeredis for unit tests).
"""

import json
import threading
import time

import redis


class WriteBehindCache:
    """Cache-aside write path + asynchronous batched database persistence."""

    DIRTY_SET = "writebehind:dirty"
    FLUSH_SET = "writebehind:flushing"

    def __init__(self, redis_client: redis.Redis, db_writer, flush_interval: float = 5.0):
        self.redis = redis_client
        self.db_writer = db_writer
        self.flush_interval = flush_interval
        self._running = True
        self._flush_thread = threading.Thread(target=self._flush_loop, daemon=True)
        self._flush_thread.start()

    def write(self, key: str, value: dict, ttl: int = 3600) -> dict:
        # Pipeline the value write and the dirty-key mark into one round trip.
        pipe = self.redis.pipeline()
        pipe.set(key, json.dumps(value), ex=ttl)
        pipe.sadd(self.DIRTY_SET, key)
        pipe.execute()
        return value

    def _flush_loop(self):
        while self._running:
            time.sleep(self.flush_interval)
            self._flush()

    def _flush(self):
        try:
            # Atomic take of the current dirty set; writes during the flush
            # land in a fresh DIRTY_SET and are picked up next cycle.
            self.redis.rename(self.DIRTY_SET, self.FLUSH_SET)
        except redis.ResponseError:
            return  # no dirty keys

        keys = self.redis.smembers(self.FLUSH_SET)
        batch = {}
        for key in keys:
            raw = self.redis.get(key)
            if raw is not None:
                batch[key] = json.loads(raw)

        try:
            if batch:
                self.db_writer(list(batch.values()))
        except Exception:
            # Merge failed keys back so they are retried next cycle.
            self.redis.sunionstore(self.DIRTY_SET, self.DIRTY_SET, self.FLUSH_SET)
            self.redis.delete(self.FLUSH_SET)
            raise

        self.redis.delete(self.FLUSH_SET)

    def flush_now(self):
        self._flush()

    def dirty_count(self) -> int:
        """Pending keys — alert when this grows without bound."""
        return self.redis.scard(self.DIRTY_SET)

    def shutdown(self):
        self._running = False
        self._flush_thread.join(timeout=10)
        self._flush()


def batch_upsert_users(db, users: list[dict]):
    """One multi-row upsert instead of N single-row updates (psycopg-style)."""
    if not users:
        return
    db.executemany(
        """
        INSERT INTO users (id, name, email)
        VALUES (%s, %s, %s)
        ON CONFLICT (id) DO UPDATE
        SET name = EXCLUDED.name, email = EXCLUDED.email
        """,
        [(u["id"], u["name"], u["email"]) for u in users],
    )


if __name__ == "__main__":
    # Demo against fakeredis if installed, else a real server.
    try:
        import fakeredis

        client = fakeredis.FakeStrictRedis(decode_responses=True)
    except ImportError:
        client = redis.Redis(host="localhost", port=6379, decode_responses=True)

    flushed = []
    cache = WriteBehindCache(client, db_writer=flushed.append, flush_interval=0.5)

    cache.write("user:1", {"id": "1", "name": "Ada", "email": "ada@example.com"})
    cache.write("user:2", {"id": "2", "name": "Grace", "email": "grace@example.com"})
    time.sleep(1.0)
    cache.shutdown()

    print(f"Flushed {len(flushed)} batch(es): {flushed}")
