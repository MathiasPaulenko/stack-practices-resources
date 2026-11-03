"""Idempotent async handler: event-hash key + Redis check-before-write.

Source: https://stackpractices.com/guides/complete-guide-aws-lambda-production/
"""
import hashlib
import json


def idempotency_key_for(event: dict) -> str:
    event_hash = hashlib.md5(
        json.dumps(event, sort_keys=True).encode()
    ).hexdigest()
    return f"idempotency:{event_hash}"


def lambda_handler(event, context, redis_client=None):
    """`redis_client` is app-provided (VPC-attached ElastiCache)."""
    key = idempotency_key_for(event)
    cached = redis_client.get(key)
    if cached:
        return {"status": "already_processed",
                "result": json.loads(cached)}

    result = process_event(event)
    redis_client.setex(key, 3600, json.dumps(result))   # TTL > retry window
    return {"status": "processed", "result": result}
