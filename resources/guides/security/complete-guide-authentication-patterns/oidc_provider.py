"""OIDC id_token verification via PyJWKClient (replaces python-jose).

Source: https://stackpractices.com/guides/complete-guide-authentication-patterns/
"""
import httpx
import jwt
from jwt import PyJWKClient
from jwt_service import AuthError


class OIDCProvider:
    def __init__(self, config: dict):
        self.config = config
        # PyJWKClient caches keys and refetches on kid rotation
        self.jwks_client = PyJWKClient(config["jwks_uri"])

    @staticmethod
    def discover_jwks_uri(issuer: str) -> str:
        resp = httpx.get(f"{issuer}/.well-known/openid-configuration")
        resp.raise_for_status()
        return resp.json()["jwks_uri"]

    def get_authorization_url(self, state: str, nonce: str) -> str:
        params = {
            "client_id": self.config["client_id"],
            "redirect_uri": self.config["redirect_uri"],
            "response_type": "code",
            "scope": "openid profile email",
            "state": state,
            "nonce": nonce,
        }
        query = "&".join(f"{k}={v}" for k, v in params.items())
        return f"{self.config['auth_url']}?{query}"

    async def exchange_code(self, code: str) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.config["token_url"],
                data={
                    "grant_type": "authorization_code",
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "redirect_uri": self.config["redirect_uri"],
                    "code": code,
                },
            )
            response.raise_for_status()
            return response.json()

    def verify_id_token(self, id_token: str, nonce: str) -> dict:
        signing_key = self.jwks_client.get_signing_key_from_jwt(id_token)
        decoded = jwt.decode(
            id_token,
            signing_key.key,
            algorithms=["RS256"],
            audience=self.config["client_id"],
            issuer=self.config["issuer"],
        )
        if decoded.get("nonce") != nonce:
            raise AuthError("Nonce mismatch")
        return decoded
