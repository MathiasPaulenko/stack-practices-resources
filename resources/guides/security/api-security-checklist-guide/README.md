# API Security Checklist — Companion Resources

Companion to the [API Security Checklist Guide](https://stackpractices.com/guides/api-security-checklist-guide/) on StackPractices.

## Files

| File | Purpose |
| --- | --- |
| `api-security-checklist.md` | Printable 40-item production checklist (English) |
| `api-security-checklist.es.md` | Printable 40-item production checklist (Spanish) |
| `helmet-config-example.js` | Production-ready Helmet configuration for Express APIs |
| `jwt-sign-example.js` | RS256 JWT signing with key rotation via `kid` header |

## Usage

1. Copy `api-security-checklist.md` into your issue tracker or print it.
2. Tick each box before deploying an API to production.
3. Use `helmet-config-example.js` as the starting point for Express security headers.
4. Use `jwt-sign-example.js` as the reference for RS256 JWT signing with key rotation.

## Sources

- [OWASP API Security Top 10](https://owasp.org/API-Security/)
- [RFC 7519 — JSON Web Token (JWT)](https://datatracker.ietf.org/doc/html/rfc7519)
- [RFC 7807 — Problem Details for HTTP APIs](https://datatracker.ietf.org/doc/html/rfc7807)
- [Helmet.js documentation](https://helmetjs.github.io/)
