"""JWT access/refresh token manager with rotation, blacklist, and reuse detection.

Companion to https://stackpractices.com/recipes/python-jwt-refresh-token-rotation/
In-memory state is fine for a single instance; use the Redis variant from the
recipe for multi-instance deployments.
"""

import secrets
import time
import uuid
from dataclasses import dataclass

import jwt


@dataclass
class TokenPair:
    access_token: str
    refresh_token: str
    access_expires_at: int
    refresh_expires_at: int


class TokenManager:
    def __init__(
        self,
        secret_key: str,
        access_token_ttl: int = 900,  # 15 minutes
        refresh_token_ttl: int = 604800,  # 7 days
        algorithm: str = "HS256",
    ):
        self.secret_key = secret_key
        self.access_token_ttl = access_token_ttl
        self.refresh_token_ttl = refresh_token_ttl
        self.algorithm = algorithm
        self._blacklist: set[str] = set()
        self._active_refresh_tokens: dict[str, dict] = {}

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

        self._active_refresh_tokens[refresh_jti] = {
            "user_id": user_id,
            "expires_at": now + self.refresh_token_ttl,
        }

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
            if payload["jti"] in self._blacklist:
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
        user_id = payload["sub"]

        if jti in self._blacklist:
            return None  # reuse detected — alert and revoke the family in production

        if jti not in self._active_refresh_tokens:
            return None

        del self._active_refresh_tokens[jti]
        self._blacklist.add(jti)
        return self.generate_tokens(user_id)

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
        if jti in self._active_refresh_tokens:
            del self._active_refresh_tokens[jti]
        self._blacklist.add(jti)
        return True

    def revoke_all_user_tokens(self, user_id: str) -> int:
        """Revoke all refresh tokens for a user. Returns the count revoked."""
        revoked = 0
        to_remove = [
            jti for jti, data in self._active_refresh_tokens.items()
            if data["user_id"] == user_id
        ]
        for jti in to_remove:
            del self._active_refresh_tokens[jti]
            self._blacklist.add(jti)
            revoked += 1
        return revoked


if __name__ == "__main__":
    manager = TokenManager(secret_key=secrets.token_urlsafe(32))

    pair = manager.generate_tokens("user123")
    print("access token (truncated):", pair.access_token[:40], "...")

    payload = manager.verify_access_token(pair.access_token)
    print("verified sub:", payload["sub"])

    rotated = manager.rotate_refresh_token(pair.refresh_token)
    print("rotated OK:", rotated is not None)

    # Reusing the old refresh token must fail (reuse detection)
    reused = manager.rotate_refresh_token(pair.refresh_token)
    print("reuse rejected:", reused is None)

    print("revoked on logout:", manager.revoke_refresh_token(rotated.refresh_token))
