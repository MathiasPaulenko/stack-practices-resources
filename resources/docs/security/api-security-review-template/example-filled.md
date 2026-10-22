# API Security Review: `payments-api`

## 1. Metadata

| Field | Value |
|-------|-------|
| API Name | `payments-api` |
| Version | `v2.4.1` |
| API Type | `REST` |
| Exposure | `Public` |
| Auth Type | `OAuth2 (client credentials + auth code w/ PKCE)` |
| Security Owner | `@m.paulenko` |
| Review Date | `2026-10-20` |

## 2. Authentication

- [x] All endpoints require authentication except explicitly documented public ones (`/health`, `/v2/docs`)
- [x] OAuth2/OIDC tokens arrive via `Authorization: Bearer`; state, PKCE, and redirect URI allowlist enforced
- [x] API keys sent in `X-Api-Key` header — never in query params
- [ ] API keys rotated every 90 days and stored in a secrets manager — **last rotation 142 days ago**
- [x] Access tokens expire in under 1 hour; refresh tokens rotate on each use and are revocable
- [x] JWT validated: signature, expiry, issuer, audience
- [x] MFA required for admin and other sensitive operations
- [ ] mTLS enforced for service-to-service communication in production — **internal hops use bearer tokens only**
- [x] Credentials never logged, returned in errors, or stored in URLs

## 3. Authorization

- [x] Access control checks the resource owner, not just authentication status (BOLA/IDOR)
- [x] Horizontal access control: User A can't read User B's `/users/{id}` data — verified with negative tests
- [x] Vertical access control: admin endpoints reject non-admin tokens
- [x] Role/permission claims validated server-side — never trusted from the client
- [ ] List and search endpoints scope results to the current caller — **`GET /v2/transactions?account_id=` accepts any account ID**
- [x] Sub-resources inherit parent permissions (e.g., `/orders/{id}/items`)
- [x] Every sensitive action audited (create, delete, bulk data access)
- [x] No auth bypass via path traversal or HTTP method override

## 4. Input Validation

- [x] All inputs validated against a strict schema (OpenAPI, JSON Schema)
- [x] Payloads with wrong types rejected — not silently coerced
- [x] Max payload size enforced at the gateway (e.g., 1 MB); limits on string, array, and nesting depth
- [x] Content-Type header checked against the actual body
- [x] Parameterized queries or ORM only — no string concatenation into SQL
- [x] Path parameters validated against expected patterns (UUID, slug, numeric)
- [x] File uploads restricted to an allowlist of names and MIME types, malware-scanned
- [x] SSRF: outbound requests validated against a domain allowlist

## 5. Rate Limiting & Abuse Prevention

| Client Type | Limit | Window | On Exceed |
|-------------|-------|--------|-----------|
| Unauthenticated | 60 req/min | 1 min | 429 + `Retry-After` |
| Authenticated | 1,000 req/min | 1 min | 429 + `Retry-After` |
| Premium | 10,000 req/min | 1 min | Graduated throttling |

- [x] Rate limits defined per consumer ID and per endpoint — not global, not IP-only
- [ ] Rate limit headers on every response — **`X-RateLimit-Reset` missing on 30% of sampled responses**
- [x] Volumetric DDoS handled at CDN/WAF layer
- [x] Account lockout after N failed authentication attempts (10 attempts / 15 min)

## 6. Secrets Management

- [x] No credentials, tokens, or signing keys in source code
- [x] Secrets injected via environment variables or a secrets manager (Vault, AWS Secrets Manager)
- [ ] JWT signing keys rotated periodically with overlap for old tokens — **no rotation policy documented**
- [x] Logs contain no tokens, passwords, or card numbers

## 7. Data Protection & Output

- [x] No sensitive data in responses (passwords, tokens, unnecessary PII)
- [x] TLS 1.2+ in transit with HSTS; AES-256 at rest
- [x] Response fields filtered by caller role — no mass assignment reads
- [x] CORS explicit allowlist — no wildcard `*` with credentials
- [x] `Cache-Control: no-store` on responses carrying sensitive data
- [x] Security headers: `X-Content-Type-Options: nosniff`, CSP `frame-ancestors` where HTML is served
- [x] PII masked or tokenized in logs

## 8. Error Handling & Logging

- [x] Error responses don't leak stack traces, SQL, or internal paths
- [x] Auth failures return generic messages (no user enumeration)
- [x] Every request logs: timestamp, client ID, endpoint, method, status code, latency
- [x] Failed authentication attempts logged with IP and timestamp
- [x] Logs forwarded to a SIEM with tamper protection; retention ≥ 90 days
- [x] Anomaly monitoring for traffic spikes and scraping patterns

## 9. OWASP API Security Top 10 (2023) Coverage

| Risk | Check | Status |
|------|-------|--------|
| API1 Broken Object Level Authorization | Owner check on every object endpoint | **Fail** — `account_id` scope gap |
| API2 Broken Authentication | Token validation, brute-force protection | Pass |
| API3 Broken Object Property Level Authorization | Response field filtering, no mass assignment | Pass |
| API4 Unrestricted Resource Consumption | Rate limits, payload caps, timeouts | Pass |
| API5 Broken Function Level Authorization | Admin functions reject non-admin callers | Pass |
| API6 Unrestricted Access to Sensitive Business Flows | Anti-automation on signup/purchase flows | Pass |
| API7 Server Side Request Forgery | Outbound URL allowlist, cloud metadata blocked | Pass |
| API8 Security Misconfiguration | No default credentials, hardened TLS | Pass |
| API9 Improper Inventory Management | Deprecated versions sunset, undocumented endpoints audited | Pass — v1 sunset 2026-08 |
| API10 Unsafe Consumption of APIs | Third-party responses validated, upstream TLS verified | Pass |

## 10. Findings & Sign-off

| # | Finding | Severity | Owner | Due | Status |
|---|---------|----------|-------|-----|--------|
| 1 | `GET /v2/transactions` accepts arbitrary `account_id` — BOLA on financial data | Blocker | `@payments-team` | 2026-10-24 | In progress |
| 2 | API key rotation overdue (142d vs 90d policy) | Medium | `@platform` | 2026-10-31 | Open |
| 3 | `X-RateLimit-Reset` missing on ~30% of responses | Low | `@gateway` | 2026-11-14 | Open |
| 4 | No mTLS between internal services | Medium | `@platform` | 2026-12-01 | Open |
| 5 | JWT signing key rotation policy undocumented | Low | `@m.paulenko` | 2026-11-07 | Open |

| Field | Value |
|-------|-------|
| Reviewer | `@m.paulenko` |
| Second reviewer | `@s.chen` (required for public APIs) |
| Result | `Blocked` — release held until finding #1 is fixed |
| Next review | `2027-01-20` |
