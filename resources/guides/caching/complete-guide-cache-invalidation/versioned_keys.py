"""Versioned cache keys — with the byte-decoding fix the article calls out.

Source: https://stackpractices.com/guides/complete-guide-cache-invalidation/
"""
import json


def get_user(r, db_users, user_id: int):
    raw = r.get(f"user_version:{user_id}")
    version = raw.decode() if raw else "1"   # r.get returns bytes!
    cache_key = f"user:{user_id}:v{version}"

    cached = r.get(cache_key)
    if cached:
        return json.loads(cached)
    user = db_users.find_by_id(user_id)
    if user:
        r.setex(cache_key, 3600, json.dumps(user))
    return user


def update_user(r, db_users, user_id: int, data: dict):
    user = db_users.update(user_id, data)
    r.incr(f"user_version:{user_id}")   # old keys become unreachable
    return user
