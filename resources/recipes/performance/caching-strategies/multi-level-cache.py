"""Multi-level caching: L1 in-process, L2 Redis, L3 database.

Usage: python multi-level-cache.py  (requires Redis on localhost:6379)
"""
import json

import redis

r = redis.Redis(decode_responses=True)


class FakeDb:
    class users:
        @staticmethod
        def find_by_id(user_id):
            return {"id": user_id, "name": f"User {user_id}"}


db = FakeDb()


def get_user(user_id):
    # L1: local in-memory cache (per process)
    if hasattr(get_user, "_cache") and user_id in get_user._cache:
        return get_user._cache[user_id]

    # L2: shared Redis cache
    key = f"user:{user_id}"
    cached = r.get(key)
    if cached:
        user = json.loads(cached)
        if not hasattr(get_user, "_cache"):
            get_user._cache = {}
        get_user._cache[user_id] = user
        return user

    # L3: database (source of truth)
    user = db.users.find_by_id(user_id)
    if user:
        r.setex(key, 3600, json.dumps(user))
        if not hasattr(get_user, "_cache"):
            get_user._cache = {}
        get_user._cache[user_id] = user
    return user


if __name__ == "__main__":
    print(get_user(7))  # L3 -> populates L2 and L1
    print(get_user(7))  # L1 hit
