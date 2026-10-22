"""Runnable JWT demo: sign, verify, refresh-flow, and blocklist.

    pip install -r requirements.txt
    python jwt_demo.py

Uses an in-memory dict for the refresh/blocklist stores; swap for Redis
or a database in production (see the recipe for the Redis variant).
"""

import jwt
import secrets
from datetime import datetime, timedelta, UTC

SECRET = "dev-only-secret-change-me-0123456789"
ALGORITHM = "HS256"
REFRESH_TTL_DAYS = 7

refresh_store: dict[str, str] = {}
blocklist: set[str] = set()


def create_access_token(user_id: str) -> str:
    payload = {
        "sub": user_id,
        "type": "access",
        "iat": datetime.now(UTC),
        "exp": datetime.now(UTC) + timedelta(minutes=15),
    }
    return jwt.encode(payload, SECRET, algorithm=ALGORITHM)


def create_refresh_token(user_id: str) -> str:
    token_id = secrets.token_urlsafe(32)
    payload = {
        "sub": user_id,
        "type": "refresh",
        "jti": token_id,
        "iat": datetime.now(UTC),
        "exp": datetime.now(UTC) + timedelta(days=REFRESH_TTL_DAYS),
    }
    token = jwt.encode(payload, SECRET, algorithm=ALGORITHM)
    refresh_store[token_id] = user_id
    return token


def verify(token: str, expected_type: str = "access") -> dict:
    claims = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
    if claims.get("type") != expected_type:
        raise ValueError(f"Not a {expected_type} token")
    if claims.get("jti") in blocklist:
        raise ValueError("Token has been revoked")
    return claims


def refresh_access_token(refresh_token: str) -> str:
    claims = verify(refresh_token, expected_type="refresh")
    if claims["jti"] not in refresh_store:
        raise ValueError("Refresh token has been revoked")
    return create_access_token(claims["sub"])


def revoke_refresh_token(refresh_token: str) -> None:
    claims = jwt.decode(refresh_token, SECRET, algorithms=[ALGORITHM])
    refresh_store.pop(claims.get("jti"), None)
    blocklist.add(claims.get("jti"))


if __name__ == "__main__":
    access = create_access_token("user-123")
    refresh = create_refresh_token("user-123")

    claims = verify(access)
    print("access token ok, sub =", claims["sub"])

    new_access = refresh_access_token(refresh)
    print("refresh flow ok, new access issued:", new_access[:30] + "...")

    revoke_refresh_token(refresh)
    try:
        refresh_access_token(refresh)
        print("ERROR: revoked refresh token still works")
    except ValueError as e:
        print("revocation ok:", e)

    try:
        verify(create_access_token("x"), expected_type="refresh")
    except ValueError as e:
        print("type check ok:", e)
