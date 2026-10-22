# API Security Review: `<API Name>`

## 1. Metadata

| Field | Value |
|-------|-------|
| API Name | `name` |
| Version | `v1.0.0` |
| API Type | `REST / GraphQL / gRPC / WebSocket` |
| Exposure | `Internal / Partner / Public` |
| Auth Type | `OAuth2 / API Key / mTLS / None` |
| Security Owner | `@name` |
| Review Date | `YYYY-MM-DD` |

## 2. Authentication

- [ ] All endpoints require authentication except explicitly documented public ones
- [ ] OAuth2/OIDC tokens arrive via `Authorization: Bearer`; state, PKCE, and redirect URI allowlist enforced
- [ ] API keys sent in `X-Api-Key` header — never in query params
- [ ] API keys rotated every 90 days and stored in a secrets manager
- [ ] Access tokens expire in under 1 hour; refresh tokens rotate on each use and are revocable
- [ ] JWT validated: signature, expiry, issuer, audience
- [ ] MFA required for admin and other sensitive operations
- [ ] mTLS enforced for service-to-service communication in production
- [ ] Credentials never logged, returned in errors, or stored in URLs

## 3. Authorization

- [ ] Access control checks the resource owner, not just authentication status (BOLA/IDOR)
- [ ] Horizontal access control: User A can't read User B's `/users/{id}` data
- [ ] Vertical access control: admin endpoints reject non-admin tokens
- [ ] Role/permission claims validated server-side — never trusted from the client
- [ ] List and search endpoints scope results to the current caller
- [ ] Sub-resources inherit parent permissions (e.g., `/orders/{id}/items`)
- [ ] Every sensitive action audited (create, delete, bulk data access)
- [ ] No auth bypass via path traversal or HTTP method override

## 4. Input Validation

- [ ] All inputs validated against a strict schema (OpenAPI, JSON Schema)
- [ ] Payloads with wrong types rejected — not silently coerced
- [ ] Max payload size enforced at the gateway (e.g., 1 MB); limits on string, array, and nesting depth
- [ ] Content-Type header checked against the actual body
- [ ] Parameterized queries or ORM only — no string concatenation into SQL
- [ ] Path parameters validated against expected patterns (UUID, slug, numeric)
- [ ] File uploads restricted to an allowlist of names and MIME types, malware-scanned
- [ ] SSRF: outbound requests validated against a domain allowlist

## 5. Rate Limiting & Abuse Prevention

| Client Type | Limit | Window | On Exceed |
|-------------|-------|--------|-----------|
| Unauthenticated | 60 req/min | 1 min | 429 + `Retry-After` |
| Authenticated | 1,000 req/min | 1 min | 429 + `Retry-After` |
| Premium | 10,000 req/min | 1 min | Graduated throttling |

- [ ] Rate limits defined per consumer ID and per endpoint — not global, not IP-only
- [ ] Rate limit headers on every response (`X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`)
- [ ] Volumetric DDoS handled at CDN/WAF layer
- [ ] Account lockout after N failed authentication attempts

## 6. Secrets Management

- [ ] No credentials, tokens, or signing keys in source code
- [ ] Secrets injected via environment variables or a secrets manager (Vault, AWS Secrets Manager)
- [ ] JWT signing keys rotated periodically with overlap for old tokens
- [ ] Logs contain no tokens, passwords, or card numbers

## 7. Data Protection & Output

- [ ] No sensitive data in responses (passwords, tokens, unnecessary PII)
- [ ] TLS 1.2+ in transit with HSTS; AES-256 at rest
- [ ] Response fields filtered by caller role — no mass assignment reads
- [ ] CORS explicit allowlist — no wildcard `*` with credentials
- [ ] `Cache-Control: no-store` on responses carrying sensitive data
- [ ] Security headers: `X-Content-Type-Options: nosniff`, CSP `frame-ancestors` where HTML is served
- [ ] PII masked or tokenized in logs

## 8. Error Handling & Logging

- [ ] Error responses don't leak stack traces, SQL, or internal paths
- [ ] Auth failures return generic messages (no user enumeration)
- [ ] Every request logs: timestamp, client ID, endpoint, method, status code, latency
- [ ] Failed authentication attempts logged with IP and timestamp
- [ ] Logs forwarded to a SIEM with tamper protection; retention ≥ 90 days
- [ ] Anomaly monitoring for traffic spikes and scraping patterns

## 9. OWASP API Security Top 10 (2023) Coverage

| Risk | Check | Status |
|------|-------|--------|
| API1 Broken Object Level Authorization | Owner check on every object endpoint | Pass / Fail |
| API2 Broken Authentication | Token validation, brute-force protection | Pass / Fail |
| API3 Broken Object Property Level Authorization | Response field filtering, no mass assignment | Pass / Fail |
| API4 Unrestricted Resource Consumption | Rate limits, payload caps, timeouts | Pass / Fail |
| API5 Broken Function Level Authorization | Admin functions reject non-admin callers | Pass / Fail |
| API6 Unrestricted Access to Sensitive Business Flows | Anti-automation on signup/purchase flows | Pass / Fail |
| API7 Server Side Request Forgery | Outbound URL allowlist, cloud metadata blocked | Pass / Fail |
| API8 Security Misconfiguration | No default credentials, hardened TLS | Pass / Fail |
| API9 Improper Inventory Management | Deprecated versions sunset, undocumented endpoints audited | Pass / Fail |
| API10 Unsafe Consumption of APIs | Third-party responses validated, upstream TLS verified | Pass / Fail |

## 10. Findings & Sign-off

| # | Finding | Severity | Owner | Due | Status |
|---|---------|----------|-------|-----|--------|
| 1 | | | | | |

| Field | Value |
|-------|-------|
| Reviewer | `@name` |
| Second reviewer | `@name` (required for public APIs) |
| Result | `Approved / Approved with exceptions / Blocked` |
| Next review | `YYYY-MM-DD` |
