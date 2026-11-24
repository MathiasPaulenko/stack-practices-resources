# Secure JWT Refresh Token Rotation with Python

Runnable companion for the StackPractices recipe:
<https://stackpractices.com/recipes/python-jwt-refresh-token-rotation/>

## Files

- `token_manager.py` — `TokenManager` class: token pair generation, access-token verification, refresh rotation with blacklist and reuse detection, single/bulk revocation. Includes a `__main__` demo that exercises the full rotation flow.
- `redis_token_manager.py` — fully wired Redis variant for multi-instance deployments: active refresh jtis live in Redis keys with TTL, rotation consumes them atomically via `GETDEL` (Redis 6.2+).
- `app.py` — FastAPI app exposing `/auth/login`, `/auth/refresh`, `/auth/logout` and a `/protected` route.

## Requirements

```bash
pip install pyjwt fastapi uvicorn
```

Optional: `cryptography` for RS256, `redis` for the distributed blacklist variant.

## Run

```bash
# demo of the rotation + reuse detection flow
python token_manager.py

# API
uvicorn app:app --reload
```

## Notes

- In-memory `_active_refresh_tokens`/`_blacklist` suit a single instance. For multi-instance deployments swap them for Redis keys with TTL (see the recipe's Redis variant).
- Reuse detection returns `None` on a blacklisted `jti` — in production, treat it as a theft signal and call `revoke_all_user_tokens`.
