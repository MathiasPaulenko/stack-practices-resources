# API Key Authentication — Companion Resources

Companion files for [Secure API Key Authentication](https://stackpractices.com/recipes/api-key-authentication/) on StackPractices.com.

## What's included

| File | Description |
|------|-------------|
| `api-key-manager.py` | `APIKeyManager` — generate/validate HMAC-signed API keys |
| `api-key-middleware.js` | Express middleware: key lookup, expiry, scope check |
| `key-hash.py` | SHA-256 hash-at-rest helper |
| `rotate-keys.py` | Dual-key rotation with grace window |

## Quick start

1. `python api-key-manager.py` — generates a sample key + validates it.
2. Wire `api-key-middleware.js` into Express with your Redis client.
3. Run `rotate-keys.py` on a schedule to retire keys past their window.
