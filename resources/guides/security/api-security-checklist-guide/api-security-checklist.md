# API Security Checklist — Production Ready (40 items)

> Companion to [API Security Checklist Guide](https://stackpractices.com/guides/api-security-checklist-guide/)
> Print this file or copy it into your issue tracker. Tick each box before going to production.

## Authentication

- [ ] JWT with RS256 (not HS256) when more than one service verifies tokens
- [ ] Token expiry: 15 min access, 7 days refresh
- [ ] Refresh token rotation on every use
- [ ] MFA for admin endpoints
- [ ] Rate limiting on login: 5 attempts, then lock 15 min
- [ ] No token in URL (use Authorization header)
- [ ] Logout invalidates token (Redis denylist via `jti`)
- [ ] Password policy: min 12 chars, complexity rules

## Authorization

- [ ] RBAC: roles user / admin / super_admin
- [ ] Verify ownership on every request (anti-IDOR)
- [ ] Scope per resource: user only accesses their data
- [ ] Deny by default, allow explicitly
- [ ] No auto-increment IDs (use UUID v4 or v7)
- [ ] Return 404 (not 403) for resources the caller doesn't own

## Input Validation

- [ ] Schema validation (Zod / pydantic) on every endpoint
- [ ] Payload size limit (max 1 MB)
- [ ] String sanitization (no HTML injection)
- [ ] Parameterized queries (anti-SQL injection)
- [ ] No eval / exec with user input
- [ ] File upload: validate type, size, content
- [ ] Reject unexpected fields (strict schema — prevents mass assignment)

## Output

- [ ] No stack traces in production
- [ ] DTO mapping: no internal fields exposed
- [ ] Security headers: X-Content-Type-Options, X-Frame-Options, CSP, HSTS
- [ ] No server / framework version exposed
- [ ] Global rate limiting: 100 req/min per user
- [ ] RFC 7807 Problem Details error format

## Transport

- [ ] TLS 1.3 mandatory (no TLS 1.0 / 1.1)
- [ ] Redirect HTTP to HTTPS
- [ ] HSTS: max-age=31536000; includeSubDomains
- [ ] Certificate pinning (mobile apps)

## Configuration

- [ ] CORS: strict origin, no wildcard
- [ ] NODE_ENV=production (or equivalent)
- [ ] Secrets in Secrets Manager (no .env in prod)
- [ ] Helmet() configured (Node.js) or equivalent security headers
- [ ] Compression with Brotli (not gzip to avoid BREACH)

## Logging and Monitoring

- [ ] Audit log of critical actions
- [ ] No logging of secrets, passwords, tokens, PII
- [ ] Alerts for failed auth attempts
- [ ] Alerts for rate limit exceeded
- [ ] SIEM integration (ELK + alerting)
- [ ] Correlation ID on every request

## Dependencies

- [ ] npm audit in CI (--audit-level=high)
- [ ] Dependabot or Snyk configured
- [ ] Lockfile committed (package-lock.json)
- [ ] License check in CI

## CI/CD

- [ ] SAST (semgrep) in pipeline
- [ ] DAST (OWASP ZAP) on staging
- [ ] Container scan (Trivy) in build
- [ ] Secret scan (git-secrets) in pre-commit
- [ ] Code review mandatory (1 approver min)
