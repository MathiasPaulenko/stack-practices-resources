# API Rate Limiting Policy — Companion Resources

Companion files for the [API Rate Limiting Policy Template](https://stackpractices.com/docs/api-rate-limiting-policy-template/).

| File | What it shows |
|------|---------------|
| `rate-limiting-policy-template.md` | The fill-in policy document (tiers, scopes, headers, escalation) |
| `express_rate_limit.js` | Redis token bucket + Express middleware with 429 headers |
| `python_rate_limit.py` | Redis token bucket in Python |
| `retry_client.js` | Client-side retry honoring `Retry-After` with jitter |
