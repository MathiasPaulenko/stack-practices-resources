"""Event-driven cache invalidation with Redis Pub/Sub.

Each app instance subscribes to the invalidation channel and drops the
affected key when an update happens — no waiting for TTLs.

Usage: run in each app instance; publish on writes.
"""
import redis

r = redis.Redis(host="localhost", port=6379, decode_responses=True)
p = r.pubsub()


def handle_invalidation(message):
    key = message["data"]
    deleted = r.delete(f"cache:product:{key}")
    if deleted:
        print(f"Invalidated cache for product {key}")


def start_listener():
    p.subscribe(**{"product-updates": handle_invalidation})
    p.run_in_thread(sleep_time=0.001)
    print("Listening for product-updates…")


def publish_update(product_id):
    # Call this wherever the product is written
    r.publish("product-updates", product_id)


if __name__ == "__main__":
    start_listener()
    publish_update(123)
