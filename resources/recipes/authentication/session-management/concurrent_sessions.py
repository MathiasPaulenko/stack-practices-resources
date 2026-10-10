"""Concurrent session control with Redis.

Caps a user at MAX_SESSIONS devices. When a new login exceeds the cap, the
oldest session IDs are evicted AND deleted from the store — trimming the
list alone doesn't invalidate them.

Usage: run Redis locally, then `python concurrent_sessions.py`.
"""

import uuid

import redis

r = redis.Redis()
MAX_SESSIONS = 3


def on_login(user_id: str) -> str:
    """Create a session, evict the oldest beyond the cap, return the new ID."""
    session_id = uuid.uuid4().hex
    r.setex(f"session:{session_id}", 3600, user_id)

    key = f"user_sessions:{user_id}"
    r.lpush(key, session_id)
    dropped = r.lrange(key, MAX_SESSIONS, -1)
    for old_id in dropped:
        r.delete(f"session:{old_id}")
    r.ltrim(key, 0, MAX_SESSIONS - 1)
    return session_id


def is_session_valid(session_id: str) -> bool:
    return bool(r.exists(f"session:{session_id}"))


if __name__ == "__main__":
    ids = [on_login("user-1") for _ in range(4)]
    for i, sid in enumerate(ids, 1):
        print(f"login {i}: {sid[:8]}... valid={is_session_valid(sid)}")
