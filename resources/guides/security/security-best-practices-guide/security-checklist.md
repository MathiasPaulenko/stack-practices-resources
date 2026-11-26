# Security Best Practices Checklist

Source: https://stackpractices.com/guides/security-best-practices-guide/

## Authentication & Authorization

- [ ] Authentication uses a proven library (no hand-rolled auth)
- [ ] Passwords hashed with Argon2id or bcrypt (per-user salt)
- [ ] MFA required for admin, production access, and financial operations
- [ ] Authorization checks resource ownership on every object-level endpoint
- [ ] Permissions audited quarterly (least privilege)
- [ ] JWTs use short expiry and asymmetric signing (RS256/ES256) when used

## Input Validation

- [ ] All input validated at the trust boundary (schema, allowlists)
- [ ] Parameterized queries everywhere (no string concatenation)
- [ ] Output encoding enabled (HTML escaping, safe JSON)
- [ ] Length and range caps on all user-controlled fields

## Secrets Management

- [ ] No secrets in source code or git history
- [ ] Secrets stored in a secrets manager (Vault, AWS SM, Doppler, etc.)
- [ ] Secret rotation scheduled (90-day baseline, immediate on exposure)
- [ ] Repo scanning in CI (gitleaks / trufflehog)

## Dependency Security

- [ ] Lock files committed (package-lock.json, poetry.lock, Cargo.lock)
- [ ] Dependency scanning in CI (npm audit, pip-audit, snyk)
- [ ] Automated update PRs enabled (Dependabot / Renovate)
- [ ] SBOM generated per release for regulated/customer-facing products

## Communication & Headers

- [ ] HTTPS enforced (301 redirect + HSTS)
- [ ] TLS 1.2+ only, weak ciphers disabled
- [ ] Security headers set (nosniff, HSTS, frame deny, CSP, Referrer-Policy)

## Rate Limiting & Logging

- [ ] Rate limiting on login, reset, and expensive endpoints
- [ ] Uniform failures on account-existence endpoints (no user enumeration)
- [ ] Auth attempts, authz failures, and validation errors logged
- [ ] No passwords, keys, PII, or card data in logs
- [ ] Log redaction at the logger; correlation IDs enabled
- [ ] Tamper-resistant or write-once log storage

Date audited: ____________  Reviewer: ____________
