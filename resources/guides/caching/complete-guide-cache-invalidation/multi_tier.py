"""Multi-tier invalidation: L2 Redis + per-instance L1 via pub/sub.

Source: https://stackpractices.com/guides/complete-guide-cache-invalidation/
"""
import threading


class MultiTierInvalidation:
    def __init__(self, redis_client, local_cache):
        self.redis = redis_client
        self.local = local_cache

    def invalidate(self, key: str):
        self.redis.delete(key)
        self.local.delete(key)
        self.redis.publish("cache-invalidation", key)

    def start_subscriber(self):
        pubsub = self.redis.pubsub()
        pubsub.subscribe("cache-invalidation")

        def listen():
            for message in pubsub.listen():
                if message["type"] == "message":
                    data = message["data"]
                    self.local.delete(
                        data.decode() if isinstance(data, bytes) else data)

        threading.Thread(target=listen, daemon=True).start()
