import jwt
from jwt import PyJWKClient

# Fetch public keys from JWKS endpoint
jwks_client = PyJWKClient('https://auth.example.com/.well-known/jwks.json')

def validate_access_token(token: str) -> dict:
    try:
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=['RS256'],
            audience='api.example.com',
            issuer='https://auth.example.com',
            options={
                'verify_exp': True,
                'verify_iat': True,
                'verify_aud': True,
                'verify_iss': True,
            },
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise AuthError('Token expired')
    except jwt.InvalidAudienceError:
        raise AuthError('Invalid audience')
    except jwt.InvalidIssuerError:
        raise AuthError('Invalid issuer')
    except jwt.InvalidTokenError:
        raise AuthError('Invalid token')
