# Complete Guide to Authentication Patterns — Companion Code

Runnable Python building blocks for the guide
[Complete Guide to Authentication Patterns](https://stackpractices.com/guides/complete-guide-authentication-patterns/)
on StackPractices.

## Files

| File | What it implements |
| --- | --- |
| `jwt_service.py` | RS256 access + refresh tokens with `type` claim separation |
| `token_rotation.py` | Refresh rotation, per-token revocation, logout-everywhere flag |
| `session_manager.py` | Redis sessions: sliding + absolute TTL, per-user session index |
| `oauth2_client.py` | Authorization Code client with `raise_for_status` |
| `oidc_provider.py` | `id_token` verification via `PyJWKClient` + nonce check |
| `passkey_manager.py` | WebAuthn registration/authentication options + verification |
| `mfa_service.py` | TOTP, hashed single-use backup codes, pending-MFA challenge |
| `abac_evaluator.py` | RBAC map + ABAC policies with `$subject.*` placeholders |
| `test_authentication.py` | pytest smoke tests (fakeredis, throwaway RSA keys) |

## Setup

```bash
pip install -r requirements.txt
pip install fakeredis pytest
pytest test_authentication.py -v
```

The modules are framework-light on purpose: `session_manager.py` and
`oauth2_client.py` assume FastAPI/`httpx`, the rest are plain Python over a
Redis client. Wire `db`, `redis`, `verify_credentials` and `get_user` to your
own data layer — those are deliberately app-provided.
