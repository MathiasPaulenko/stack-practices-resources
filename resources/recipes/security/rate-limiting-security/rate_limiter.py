"""Atomic token-bucket rate limiter using a Redis Lua script.

Usage:
    pip install redis
    python rate_limiter.py
"""
import time

import redis

r = redis.Redis(host="localhost", port=6379, db=0)
TOKEN_BUCKET = r.register_script(open("token_bucket.lua").read())


def is_allowed(key: str, capacity: int, refill_rate: float, ttl: int = 60) -> bool:
    """Return True if the request under `key` is within the limit."""
    return bool(
        TOKEN_BUCKET(keys=[key], args=[capacity, refill_rate, time.time(), ttl])
    )


def login_rate_limit(client_ip: str, account: str) -> bool:
    """5 login attempts per minute per IP + account pair."""
    key = f"rl:login:{client_ip}:{account}"
    return is_allowed(key, capacity=5, refill_rate=5 / 60)


if __name__ == "__main__":
    for i in range(8):
        ok = login_rate_limit("203.0.113.7", "user@example.com")
        print(f"attempt {i + 1}: {'allowed' if ok else 'RATE LIMITED'}")
