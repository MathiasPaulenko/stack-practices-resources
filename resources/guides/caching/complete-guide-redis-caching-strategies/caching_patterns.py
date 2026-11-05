"""Redis caching patterns — companion to the StackPractices guide.

All snippets expect a `db` object exposing users.find_by_id() / users.update().
Requires redis-py >= 4.1 (scan_iter, redis.cluster).
"""

import json
import logging
import queue
import random
import threading
import time

import redis

log = logging.getLogger(__name__)
r = redis.Redis(host="localhost", port=6379, db=0)

# ---------------------------------------------------------------- cache-aside

def get_user(user_id: int) -> dict | None:
    cache_key = f"user:{user_id}"
    cached = r.get(cache_key)
    if cached:
        return json.loads(cached)
    user = db.users.find_by_id(user_id)
    if user:
        r.setex(cache_key, 3600, json.dumps(user))
    return user


def update_user(user_id: int, data: dict) -> dict:
    user = db.users.update(user_id, data)
    r.delete(f"user:{user_id}")
    return user


def get_user_safe(user_id: int, max_wait_s: float = 2.0) -> dict | None:
    cache_key = f"user:{user_id}"
    lock_key = f"lock:{cache_key}"
    deadline = time.monotonic() + max_wait_s

    cached = r.get(cache_key)
    if cached:
        return json.loads(cached)

    while time.monotonic() < deadline:
        if r.set(lock_key, "1", nx=True, ex=10):
            try:
                cached = r.get(cache_key)
                if cached:
                    return json.loads(cached)
                user = db.users.find_by_id(user_id)
                if user:
                    r.setex(cache_key, 3600, json.dumps(user))
                return user
            finally:
                r.delete(lock_key)
        time.sleep(0.05 + random.random() * 0.05)

    return db.users.find_by_id(user_id)


# ---------------------------------------------------------------- read-through

class ReadThroughCache:
    def __init__(self, redis_client, db_loader):
        self.redis = redis_client
        self.db_loader = db_loader

    def get(self, key: str, ttl: int = 3600) -> dict | None:
        cached = self.redis.get(key)
        if cached:
            return json.loads(cached)
        data = self.db_loader(key)
        if data is not None:
            self.redis.setex(key, ttl, json.dumps(data))
        return data


# ---------------------------------------------------------------- write-through

class WriteThroughCache:
    """DB-then-cache ordering: the cache only holds committed data."""

    def __init__(self, redis_client, db_writer):
        self.redis = redis_client
        self.db_writer = db_writer

    def set(self, key: str, value: dict, ttl: int = 3600) -> dict:
        result = self.db_writer(key, value)
        self.redis.setex(key, ttl, json.dumps(result))
        return result


# ---------------------------------------------------------------- write-behind

write_queue: queue.Queue = queue.Queue()


def flush_worker(db_writer, batch_size: int = 50):
    while True:
        batch = [write_queue.get() for _ in range(batch_size)]
        try:
            db_writer(batch)
        except Exception:
            log.exception("write-behind flush failed for %d keys", len(batch))
        finally:
            for _ in batch:
                write_queue.task_done()


def write_behind_set(key: str, value: dict, ttl: int = 3600):
    r.setex(key, ttl, json.dumps(value))
    write_queue.put((key, value))


# ---------------------------------------------------------------- refresh-ahead

def refresh_ahead(redis_client, db_loader, pattern: str = "user:*",
                  ttl: int = 3600, horizon_s: int = 300, interval_s: int = 60):
    while True:
        for key in redis_client.scan_iter(match=pattern, count=200):
            remaining = redis_client.ttl(key)
            if 0 < remaining < horizon_s:
                data = db_loader(key)
                if data is not None:
                    redis_client.setex(key, ttl, json.dumps(data))
        time.sleep(interval_s)


# ---------------------------------------------------------------- ttl jitter

def set_with_jitter(key: str, value: str, base_ttl: int = 3600, jitter: int = 300):
    r.setex(key, base_ttl + random.randint(0, jitter), value)
