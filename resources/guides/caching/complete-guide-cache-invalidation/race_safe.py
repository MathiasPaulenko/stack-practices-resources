"""Race-safe reads: lock + double-check, and delayed double-delete on writes.

Source: https://stackpractices.com/guides/complete-guide-cache-invalidation/
"""
import json
import threading
import time


def get_safe(r, db_users, user_id: int, retries: int = 3):
    cache_key = f"user:{user_id}"
    lock_key = f"lock:{cache_key}"

    cached = r.get(cache_key)
    if cached:
        return json.loads(cached)

    if r.set(lock_key, "1", nx=True, ex=10):
        try:
            cached = r.get(cache_key)      # double-check under lock
            if cached:
                return json.loads(cached)
            user = db_users.find_by_id(user_id)
            if user:
                r.setex(cache_key, 3600, json.dumps(user))
            return user
        finally:
            r.delete(lock_key)
    elif retries > 0:
        time.sleep(0.05)
        return get_safe(r, db_users, user_id, retries - 1)
    return db_users.find_by_id(user_id)    # give up: read origin directly


def update_safe(r, db_users, user_id: int, data: dict,
                delay: float = 0.5):
    r.delete(f"user:{user_id}")                    # before write
    user = db_users.update(user_id, data)
    threading.Timer(delay, r.delete,
                    args=[f"user:{user_id}"]).start()   # after write
    return user
