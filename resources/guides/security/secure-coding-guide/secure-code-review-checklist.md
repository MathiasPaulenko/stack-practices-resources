# Secure Code Review Checklist

Production-ready checklist for reviewing code before release. Tick each item; anything unchecked is a finding to document or fix.

## Input

- [ ] Schema validation on every payload (zod `safeParse`, pydantic, Bean Validation)
- [ ] String sanitization where HTML is rendered (DOMPurify or equivalent)
- [ ] Parameterized queries everywhere — zero string-concatenated SQL
- [ ] File uploads: size limit, real MIME sniffing, stored outside web root

## Authentication & Authorization

- [ ] Auth token verified on every request (no "the gateway does it" assumptions)
- [ ] RBAC + scope checked per resource, not per route group
- [ ] Ownership verified — the user can only touch their own objects (IDOR check)
- [ ] Rate limiting on login, signup, and reset endpoints
- [ ] Passwords hashed with bcrypt/Argon2id (cost factor documented)

## Output

- [ ] No stack traces or internals in error responses
- [ ] No sensitive fields in API responses (DTO/mapping layer)
- [ ] Security headers set (CSP, X-Frame-Options/frame-ancestors, nosniff)

## Session

- [ ] Token expiry documented and short (15–60 min access tokens)
- [ ] Refresh token rotation implemented
- [ ] Logout actually invalidates the token server-side

## Logging

- [ ] No secrets, tokens, or PII in logs (logger-level redaction)
- [ ] Audit log for critical actions AND unauthorized attempts

## Dependencies

- [ ] Dependency scan in CI (`npm audit`, `pip-audit`, `cargo audit`, Snyk)
- [ ] Secret scanning in CI (gitleaks, trufflehog)
- [ ] Lockfile committed; no floating `latest` versions

## Configuration

- [ ] Production mode enforced (`NODE_ENV=production` or equivalent)
- [ ] CORS restricted to known origins
- [ ] TLS 1.2+ mandatory; HSTS enabled
