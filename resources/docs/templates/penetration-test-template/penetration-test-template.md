# Penetration Test Report

## Executive Summary

| Field | Value |
|-------|-------|
| **Target** | [application / network / API] |
| **Scope** | [in-scope and out-of-scope URLs / IPs] |
| **Test period** | [YYYY-MM-DD to YYYY-MM-DD] |
| **Tester** | [internal team / vendor] |
| **Aggregate risk** | [Critical / High / Medium / Low] |

## Risk Summary

| Severity | Count | Status |
|----------|-------|--------|
| Critical | [N] | [open / remediated] |
| High | [N] | [open / remediated] |
| Medium | [N] | [open / remediated] |
| Low | [N] | [open / remediated] |
| Informational | [N] | [open / remediated] |

## Finding Template

### [FINDING-001] [Title]

| Field | Value |
|-------|-------|
| **Severity** | [Critical / High / Medium / Low / Info] |
| **CVSS** | [score] |
| **Category** | [OWASP category] |
| **Status** | [open / remediated / accepted risk] |

#### Description
What the vulnerability is and why it matters.

#### Affected Resources
- URL: `https://example.com/api/v1/users`
- Parameter: `id`
- Component: User controller

#### Proof of Concept
```bash
curl "https://example.com/api/v1/users?id=1 OR 1=1"
# Returns all users — SQL injection confirmed
```

#### Impact
What an attacker could do with this vulnerability.

#### Remediation
Specific steps to fix. Include code examples if applicable.

#### References
- OWASP: [link]
- CVE: [if applicable]

## Remediation Tracking

| ID | Finding | Owner | Due Date | Status |
|----|---------|-------|----------|--------|
| 001 | SQL Injection | Backend team | +7 days | In progress |
| 002 | XSS | Frontend team | +14 days | Open |

## Risk Rating Matrix

| Likelihood \ Impact | Low | Medium | High |
|---------------------|-----|--------|------|
| High | Medium | High | Critical |
| Medium | Low | Medium | High |
| Low | Info | Low | Medium |
