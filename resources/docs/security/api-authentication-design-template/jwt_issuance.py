import jwt
from datetime import datetime, timedelta, timezone
from cryptography.hazmat.primitives import serialization

def issue_access_token(user_id: str, scopes: list[str]) -> str:
    private_key = load_private_key()  # From secrets manager

    now = datetime.now(timezone.utc)
    payload = {
        'iss': 'https://auth.example.com',
        'sub': user_id,
        'aud': ['api.example.com'],
        'exp': now + timedelta(minutes=15),
        'iat': now,
        'nbf': now,
        'jti': str(uuid.uuid4()),
        'scope': ' '.join(scopes),
    }

    return jwt.encode(
        payload,
        private_key,
        algorithm='RS256',
        headers={'kid': 'key-v2'},
    )

def issue_refresh_token(user_id: str) -> str:
    # Refresh token is opaque (not JWT) — stored server-side
    token = secrets.token_urlsafe(48)
    store_refresh_token(token, user_id, expires_in=timedelta(days=7))
    return token
