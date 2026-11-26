# Security Audit Checklist

Scope: `<System/Organization Name>` | Auditor: `<Name>` | Date: `<YYYY-MM-DD>`

## 1. Network Security

- [ ] Firewall rules documented and in version control
- [ ] Default deny policy; no any-any rules
- [ ] Firewall rules reviewed quarterly; no unused rules
- [ ] Management access restricted (VPN / jump host only)
- [ ] DMZ configured; production and DB networks isolated
- [ ] Kubernetes NetworkPolicies (default deny between namespaces)
- [ ] DNSSEC on public zones; DNS filtering and logging
- [ ] DDoS mitigation at the edge; rate limiting on APIs

## 2. Application Security

- [ ] MFA enforced for all users (TOTP or hardware key)
- [ ] Passwords hashed with Argon2id/bcrypt; breach check
- [ ] Session management: idle + absolute timeouts, Secure cookies
- [ ] RBAC enforced server-side; least privilege
- [ ] Quarterly access reviews; JIT for privileged access
- [ ] Parameterized queries everywhere (no string-built SQL)
- [ ] Output encoding + CSP against XSS
- [ ] SameSite cookies + CSRF tokens on state changes
- [ ] File upload validation (type, size, malware scan)
- [ ] SSRF allowlist for outbound requests
- [ ] Security headers: CSP, HSTS, X-Content-Type-Options, X-Frame-Options
- [ ] Dependency scan in CI; 0 critical/high threshold
- [ ] SBOM generated per release; container images scanned

## 3. Data Protection

- [ ] TLS 1.2+ everywhere; SSLv3 / TLS 1.0/1.1 disabled
- [ ] Certificates auto-renewed; expiry alerting
- [ ] Encryption at rest: databases, object storage, volumes
- [ ] Field-level encryption for PII
- [ ] Data classification applied; PII identified and tagged
- [ ] Retention policy enforced automatically; secure deletion
- [ ] Backups encrypted; restore tested monthly
- [ ] No secrets in code, logs, or .env files
- [ ] Secrets in a vault; rotation automated; access logged

## 4. Infrastructure Security

- [ ] CIS benchmarks applied; drift monitored
- [ ] No public buckets or databases; private subnets only
- [ ] IAM least privilege; no wildcard permissions in prod
- [ ] CloudTrail / audit logs in all regions with integrity checks
- [ ] Pod Security Standards (Restricted); no privileged/root containers
- [ ] readOnlyRootFilesystem; admission controllers (Kyverno/OPA)
- [ ] OS baseline hardened; unnecessary services disabled
- [ ] SSH key-only; PermitRootLogin no; fail2ban
- [ ] Automatic security updates; file integrity monitoring; host IDS

## 5. Monitoring & Logging

- [ ] All log sources feed the SIEM (app, access, audit, firewall, cloud)
- [ ] Retention policy per log type (audit logs >= 1 year)
- [ ] Alerts for brute force, privilege escalation, exfiltration, malware
- [ ] False positive rate < 5%; alert fatigue monitored
- [ ] Threat intel feed integrated; incidents tracked to closure

## 6. Incident Response

- [ ] IR plan documented and current
- [ ] IR team defined with 24/7 on-call coverage
- [ ] Escalation path per severity; contact list updated monthly
- [ ] Tabletop exercise in the last 6 months
- [ ] Post-incident reviews (blameless) for every incident
- [ ] MTTD / MTTR tracked against targets

## 7. Compliance

- [ ] SOC 2 controls mapped to evidence (CC6.x, CC7.x, CC8.1)
- [ ] ROPA current; consent management; DSR SLA met
- [ ] 72-hour breach notification procedure tested
- [ ] ISO 27001 Annex A controls reviewed annually
- [ ] Third-party vendors with data access have DPA/BAA
- [ ] External penetration test within the last 12 months

## Findings

| # | Finding | Severity | Evidence | Owner | Due date |
|---|---------|----------|----------|-------|----------|
| 1 | | | | | |
