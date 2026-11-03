"""JWT service: RS256 access + refresh tokens with typed claims.

Source: https://stackpractices.com/guides/complete-guide-authentication-patterns/
"""
import secrets
import jwt
from datetime import datetime, timedelta, timezone
from dataclasses import dataclass


class AuthError(Exception):
    pass


@dataclass
class JWTConfig:
    private_key: str
    public_key: str
    issuer: str = "https://auth.example.com"
    audience: str = "example-api"
    access_token_ttl: int = 900          # 15 minutes
    refresh_token_ttl: int = 86400 * 7   # 7 days


class JWTService:
    def __init__(self, config: JWTConfig):
        self.config = config

    def generate_access_token(self, user_id: str, claims: dict) -> str:
        now = datetime.now(timezone.utc)
        payload = {
            "sub": user_id,
            "iss": self.config.issuer,
            "aud": self.config.audience,
            "iat": now,
            "nbf": now,
            "exp": now + timedelta(seconds=self.config.access_token_ttl),
            "type": "access",
            **claims,
        }
        return jwt.encode(payload, self.config.private_key, algorithm="RS256")

    def generate_refresh_token(self, user_id: str) -> str:
        now = datetime.now(timezone.utc)
        payload = {
            "sub": user_id,
            "iss": self.config.issuer,
            "aud": self.config.audience,
            "iat": now,
            "exp": now + timedelta(seconds=self.config.refresh_token_ttl),
            "type": "refresh",
            "jti": secrets.token_urlsafe(16),
        }
        return jwt.encode(payload, self.config.private_key, algorithm="RS256")

    def verify_token(self, token: str, expected_type: str = "access") -> dict:
        try:
            payload = jwt.decode(
                token,
                self.config.public_key,
                algorithms=["RS256"],
                issuer=self.config.issuer,
                audience=self.config.audience,
                options={"require": ["exp", "iss", "aud", "sub", "type"]},
            )
            if payload.get("type") != expected_type:
                raise AuthError(
                    f"Expected {expected_type} token, got {payload.get('type')}"
                )
            return payload
        except jwt.ExpiredSignatureError:
            raise AuthError("Token expired")
        except jwt.InvalidTokenError as e:
            raise AuthError(f"Invalid token: {e}")
