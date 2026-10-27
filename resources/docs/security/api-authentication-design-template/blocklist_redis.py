import redis
import time

r = redis.Redis(host='redis', port=6379, db=0)

def revoke_token(jti: str, exp: int):
    # Store jti in Redis with TTL matching token expiry
    ttl = exp - int(time.time())
    if ttl > 0:
        r.setex(f'revoked:{jti}', ttl, '1')

def is_token_revoked(jti: str) -> bool:
    return r.exists(f'revoked:{jti}') > 0

# In token validation
def validate_access_token(token: str) -> dict:
    payload = decode_jwt(token)
    if is_token_revoked(payload['jti']):
        raise AuthError('Token revoked')
    return payload
