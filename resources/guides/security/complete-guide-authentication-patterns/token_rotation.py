"""Refresh token rotation with per-user global revocation.

Source: https://stackpractices.com/guides/complete-guide-authentication-patterns/
"""
from jwt_service import JWTService, AuthError


class TokenRotationManager:
    def __init__(self, jwt_service: JWTService, redis_client):
        self.jwt = jwt_service
        self.redis = redis_client

    def refresh_tokens(self, refresh_token: str) -> dict:
        payload = self.jwt.verify_token(refresh_token, expected_type="refresh")
        jti = payload["jti"]
        user_id = payload["sub"]

        # Global revocation must be checked BEFORE the per-token check.
        if self.redis.get(f"revoked_user:{user_id}"):
            raise AuthError("All tokens for this user have been revoked")
        if self.redis.get(f"revoked:{jti}"):
            raise AuthError("Refresh token has been revoked")

        self.redis.setex(f"revoked:{jti}", self.jwt.config.refresh_token_ttl, "1")
        return {
            "access_token": self.jwt.generate_access_token(user_id, {}),
            "refresh_token": self.jwt.generate_refresh_token(user_id),
            "expires_in": self.jwt.config.access_token_ttl,
        }

    def revoke_all_tokens(self, user_id: str):
        """Logout everywhere: flag the user so every refresh token dies."""
        self.redis.setex(
            f"revoked_user:{user_id}", self.jwt.config.refresh_token_ttl, "1"
        )

    def logout(self, refresh_token: str):
        payload = self.jwt.verify_token(refresh_token, expected_type="refresh")
        self.redis.setex(
            f"revoked:{payload['jti']}", self.jwt.config.refresh_token_ttl, "1"
        )
