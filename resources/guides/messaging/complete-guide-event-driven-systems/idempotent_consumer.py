"""Idempotent event consumer: Redis dedup key + conditional state update."""
import redis

r = redis.Redis(host="redis", port=6379)
DEDUP_TTL_SECONDS = 86400


def process_event_idempotent(event: dict) -> dict:
    """Skip duplicates with an atomic SETNX; delete the key on failure to allow retry."""
    event_id = event["event_id"]

    if not r.setnx(f"processed:{event_id}", "1"):
        return {"status": "duplicate"}

    r.expire(f"processed:{event_id}", DEDUP_TTL_SECONDS)

    try:
        result = handle_event(event)
        return {"status": "processed", "result": result}
    except Exception:
        r.delete(f"processed:{event_id}")
        raise


def handle_event(event: dict):
    raise NotImplementedError("plug in your handler")
