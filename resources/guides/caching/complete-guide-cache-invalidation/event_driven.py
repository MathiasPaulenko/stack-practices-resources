"""Event-driven invalidation: write-then-delete + pub/sub broadcast.

Source: https://stackpractices.com/guides/complete-guide-cache-invalidation/
"""
import threading


def write_then_delete(r, db_users, user_id: int, data: dict) -> dict:
    user = db_users.update(user_id, data)   # 1. write first
    r.delete(f"user:{user_id}")           # 2. then invalidate
    return user


def invalidate_cache(r, key: str):
    r.delete(key)
    r.publish("cache-invalidation", key)


def invalidation_subscriber(r, local_cache):
    pubsub = r.pubsub()
    pubsub.subscribe("cache-invalidation")
    for message in pubsub.listen():
        if message["type"] == "message":
            data = message["data"]
            local_cache.delete(
                data.decode() if isinstance(data, bytes) else data)


def start_subscriber(r, local_cache):
    threading.Thread(target=invalidation_subscriber,
                     args=(r, local_cache), daemon=True).start()
