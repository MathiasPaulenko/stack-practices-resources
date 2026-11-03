# API Security — Companion

Runnable security controls from the [Complete Guide to API Security](https://stackpractices.com/guides/complete-guide-api-security/).

## Files

- `token_bucket_limiter.py` — in-memory token-bucket limiter + FastAPI middleware
- `redis_rate_limiter.py` — sliding-window limiter on Redis sorted sets
- `tiered_limiter.py` — per-plan rate limits (free/pro/enterprise)
- `pydantic_validation.py` — schema validation with Pydantic v2 (Field, field_validator)
- `file_upload_validation.py` — magic-bytes MIME checks + safe filenames
- `cors_config.py` — strict CORS setup
- `sql_injection_prevention.py` — vulnerable vs safe query patterns + allowlists
- `mass_assignment_protection.py` — explicit update schemas, model_dump
- `gateway_middleware.py` — size limits, API keys, rate limits, security headers
- `pagination_security.py` — page-size caps + hardened cursor pagination
- `audit_logging.py` — structured audit log + security events
- `test_api_security.py` — pytest suite: injection, mass assignment, CORS, auth, pagination

## Usage

Requires `fastapi`, `pydantic>=2`, `redis`, `python-magic`, `pytest`, `httpx`. Copy what you need; run tests with `pytest test_api_security.py` against your app fixtures.
