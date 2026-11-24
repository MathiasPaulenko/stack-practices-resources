"""Redis-backed variant of TokenManager for multi-instance deployments.

Companion to https://stackpractices.com/recipes/python-jwt-refresh-token-rotation/
Replaces the in-memory _active_refresh_tokens/_blacklist with Redis keys that
expire with the token TTL, so every server instance shares rotation state.

Requires: pip install redis pyjwt
"""

import json
import secrets
import time
import uuid
from dataclasses import dataclass

import jwt
import redis


@dataclass
class TokenPair:
    access_token: str
    refresh_token: str
    access_expires_at: int
    refresh_expires_at: int


class RedisTokenManager:
    def __init__(
        self,
        secret_key: str,
        redis_url: str = "redis://localhost:6379",
        access_token_ttl: int = 900,  # 15 minutes
        refresh_token_ttl: int = 604800,  # 7 days
        algorithm: str = "HS256",
    ):
        self.secret_key = secret_key
        self.access_token_ttl = access_token_ttl
        self.refresh_token_ttl = refresh_token_ttl
        self.algorithm = algorithm
        self.redis = redis.from_url(redis_url)

    def _blacklist_token(self, jti: str, expires_at: int) -> None:
        ttl = max(expires_at - int(time.time()), 1)
        self.redis.setex(f"blacklist:{jti}", ttl, "1")

    def _is_blacklisted(self, jti: str) -> bool:
        return bool(self.redis.exists(f"blacklist:{jti}"))

    def _store_active(self, jti: str, user_id: str, expires_at: int) -> None:
        ttl = max(expires_at - int(time.time()), 1)
        self.redis.setex(f"refresh:{jti}", ttl, json.dumps({"user_id": user_id}))

    def _pop_active(self, jti: str) -> dict | None:
        """Atomically read-and-delete an active refresh jti (GETDEL needs Redis 6.2+)."""
        raw = self.redis.getdel(f"refresh:{jti}")
        return json.loads(raw) if raw else None

    def generate_tokens(self, user_id: str, claims: dict | None = None) -> TokenPair:
        """Generate a new access and refresh token pair."""
        now = int(time.time())
        access_jti = str(uuid.uuid4())
        refresh_jti = str(uuid.uuid4())

        access_payload = {
            "sub": user_id,
            "jti": access_jti,
            "type": "access",
            "iat": now,
            "exp": now + self.access_token_ttl,
            **(claims or {}),
        }
        refresh_payload = {
            "sub": user_id,
            "jti": refresh_jti,
            "type": "refresh",
            "iat": now,
            "exp": now + self.refresh_token_ttl,
        }

        access_token = jwt.encode(access_payload, self.secret_key, algorithm=self.algorithm)
        refresh_token = jwt.encode(refresh_payload, self.secret_key, algorithm=self.algorithm)

        self._store_active(refresh_jti, user_id, now + self.refresh_token_ttl)

        return TokenPair(
            access_token=access_token,
            refresh_token=refresh_token,
            access_expires_at=now + self.access_token_ttl,
            refresh_expires_at=now + self.refresh_token_ttl,
        )

    def verify_access_token(self, token: str) -> dict | None:
        """Verify an access token and return its payload, or None."""
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm],
            )
            if payload.get("type") != "access":
                return None
            if self._is_blacklisted(payload["jti"]):
                return None
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    def rotate_refresh_token(self, refresh_token: str) -> TokenPair | None:
        """Rotate a refresh token — issue a new pair and blacklist the old jti."""
        try:
            payload = jwt.decode(
                refresh_token,
                self.secret_key,
                algorithms=[self.algorithm],
            )
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return None

        if payload.get("type") != "refresh":
            return None

        jti = payload["jti"]

        if self._is_blacklisted(jti):
            return None  # reuse detected — alert and revoke the family in production

        # GETDEL makes the check-and-consume atomic across instances.
        active = self._pop_active(jti)
        if active is None:
            return None

        self._blacklist_token(jti, payload["exp"])
        return self.generate_tokens(active["user_id"])

    def revoke_refresh_token(self, refresh_token: str) -> bool:
        """Revoke a refresh token (logout). Returns True if a valid refresh token was revoked."""
        try:
            payload = jwt.decode(
                refresh_token,
                self.secret_key,
                algorithms=[self.algorithm],
            )
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return False

        if payload.get("type") != "refresh":
            return False

        jti = payload["jti"]
        self.redis.delete(f"refresh:{jti}")
        self._blacklist_token(jti, payload["exp"])
        return True

    def revoke_all_user_tokens(self, user_id: str) -> int:
        """Revoke all refresh tokens for a user. Returns the count revoked."""
        revoked = 0
        for key in self.redis.scan_iter("refresh:*"):
            raw = self.redis.get(key)
            if raw and json.loads(raw)["user_id"] == user_id:
                jti = key.split(":", 1)[1]
                # key value holds the payload-free dict; use the stored TTL as expiry hint
                ttl = self.redis.ttl(key)
                self.redis.delete(key)
                self._blacklist_token(jti, int(time.time()) + max(ttl, 1))
                revoked += 1
        return revoked


if __name__ == "__main__":
    manager = RedisTokenManager(
        secret_key=secrets.token_urlsafe(32),
        redis_url="redis://localhost:6379",
    )

    pair = manager.generate_tokens("user123")
    rotated = manager.rotate_refresh_token(pair.refresh_token)
    print("rotated OK:", rotated is not None)
    print("reuse rejected:", manager.rotate_refresh_token(pair.refresh_token) is None)
    print("revoked on logout:", manager.revoke_refresh_token(rotated.refresh_token))
