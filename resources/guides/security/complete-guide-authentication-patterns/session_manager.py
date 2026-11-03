"""Redis-backed session manager with sliding + absolute TTL.

Source: https://stackpractices.com/guides/complete-guide-authentication-patterns/
"""
import secrets
from datetime import datetime, timezone
from fastapi import Request, Response


class SessionManager:
    def __init__(self, db, redis_client):
        self.db = db
        self.redis = redis_client
        self.session_ttl = 3600
        self.absolute_ttl = 86400 * 14
        self.cookie_name = "session_id"

    def create_session(self, response: Response, user_id: str) -> str:
        session_id = secrets.token_urlsafe(32)
        self.redis.hset(
            f"session:{session_id}",
            mapping={
                "user_id": user_id,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "last_access": datetime.now(timezone.utc).isoformat(),
            },
        )
        self.redis.expire(f"session:{session_id}", self.absolute_ttl)
        self.redis.sadd(f"user_sessions:{user_id}", session_id)
        response.set_cookie(
            key=self.cookie_name,
            value=session_id,
            httponly=True,
            secure=True,
            samesite="strict",
            max_age=self.absolute_ttl,
            path="/",
        )
        return session_id

    def get_session(self, request: Request) -> dict | None:
        session_id = request.cookies.get(self.cookie_name)
        if not session_id:
            return None
        session_data = self.redis.hgetall(f"session:{session_id}")
        if not session_data:
            return None
        self.redis.hset(
            f"session:{session_id}",
            "last_access",
            datetime.now(timezone.utc).isoformat(),
        )
        return session_data

    def destroy_session(self, request: Request, response: Response):
        session_id = request.cookies.get(self.cookie_name)
        if not session_id:
            return
        session_data = self.redis.hgetall(f"session:{session_id}")
        user_id = session_data.get("user_id")
        self.redis.delete(f"session:{session_id}")
        if user_id:
            self.redis.srem(f"user_sessions:{user_id}", session_id)
        response.delete_cookie(self.cookie_name, path="/")

    def destroy_all_sessions(self, user_id: str):
        for session_id in self.redis.smembers(f"user_sessions:{user_id}"):
            self.redis.delete(f"session:{session_id}")
        self.redis.delete(f"user_sessions:{user_id}")
