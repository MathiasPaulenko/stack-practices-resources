# Example Penetration Test Report: payment-service

This is a filled-in example based on the penetration-test-template.md. Use it as a reference for what a completed report looks like.

## Executive Summary

| Field | Value |
|-------|-------|
| **Target** | payment-service API |
| **Scope** | https://api.company.com/payments/* and https://api.company.com/orders/* |
| **Test period** | 2026-08-15 to 2026-08-19 |
| **Tester** | Security Firm XYZ |
| **Aggregate risk** | High |

## Risk Summary

| Severity | Count | Status |
|----------|-------|--------|
| Critical | 1 | open |
| High | 2 | 1 remediated, 1 open |
| Medium | 3 | 2 remediated, 1 open |
| Low | 4 | all remediated |
| Informational | 2 | all remediated |

## Findings

### [FINDING-001] SQL Injection in orders endpoint

| Field | Value |
|-------|-------|
| **Severity** | Critical |
| **CVSS** | 9.8 |
| **Category** | OWASP A03:2021 — Injection |
| **Status** | open |

#### Description
The `GET /orders/search` endpoint accepts a `q` parameter that is concatenated directly into a SQL query without parameterization. An attacker can inject arbitrary SQL to read, modify, or delete data.

#### Affected Resources
- URL: `https://api.company.com/orders/search?q=`
- Parameter: `q`
- Component: OrderSearchController

#### Proof of Concept
```bash
curl "https://api.company.com/orders/search?q=' UNION SELECT username,password_hash FROM users--"
# Returns user credentials from the database
```

#### Impact
Full database read access. An attacker can exfiltrate all user data, payment records, and credentials. This is a PCI DSS violation (Requirement 6.5.1).

#### Remediation
Use parameterized queries instead of string concatenation.

Python example:
```python
# Vulnerable
cursor.execute(f"SELECT * FROM orders WHERE description LIKE '%{q}%'")

# Fixed
cursor.execute("SELECT * FROM orders WHERE description LIKE %s", (f"%{q}%",))
```

Java example:
```java
// Vulnerable
String sql = "SELECT * FROM orders WHERE description LIKE '%" + q + "%'";
statement.executeQuery(sql);

// Fixed
PreparedStatement ps = conn.prepareStatement("SELECT * FROM orders WHERE description LIKE ?");
ps.setString(1, "%" + q + "%");
ps.executeQuery();
```

#### References
- OWASP A03:2021: https://owasp.org/Top10/A03_2021-Injection/
- CWE-89: https://cwe.mitre.org/data/definitions/89.html
- PCI DSS 6.5.1

### [FINDING-002] Missing rate limiting on login endpoint

| Field | Value |
|-------|-------|
| **Severity** | High |
| **CVSS** | 7.5 |
| **Category** | OWASP API4:2023 — Unrestricted Resource Consumption |
| **Status** | remediated |

#### Description
The `POST /auth/login` endpoint has no rate limiting. An attacker can brute-force passwords at high speed.

#### Affected Resources
- URL: `https://api.company.com/auth/login`
- Parameter: N/A
- Component: AuthController

#### Proof of Concept
```bash
# 1000 requests in 10 seconds — no 429 response
for i in $(seq 1 1000); do
  curl -s -o /dev/null -w "%{http_code}\n" -X POST https://api.company.com/auth/login \
    -H "Content-Type: application/json" \
    -d '{"email":"admin@company.com","password":"guess'$i'"}'
done
```

#### Impact
Credential stuffing and brute-force attacks succeed without throttling.

#### Remediation
Add rate limiting with a token bucket (e.g., Redis + aiolimiter or nginx limit_req).

```nginx
limit_req_zone $binary_remote_addr zone=login:10m rate=10r/m;

location /auth/login {
  limit_req zone=login burst=5 nodelay;
  proxy_pass http://backend;
}
```

#### References
- OWASP API4:2023: https://owasp.org/API-Security/editions/2023/en/0x11-t10/
- CWE-307: https://cwe.mitre.org/data/definitions/307.html

### [FINDING-003] CORS misconfiguration allows wildcard origins

| Field | Value |
|-------|-------|
| **Severity** | Medium |
| **CVSS** | 5.4 |
| **Category** | OWASP A05:2021 — Security Misconfiguration |
| **Status** | remediated |

#### Description
The API returns `Access-Control-Allow-Origin: *` with `Access-Control-Allow-Credentials: true`, which violates the CORS specification and allows any website to make authenticated requests.

#### Affected Resources
- URL: All API endpoints
- Parameter: N/A
- Component: CORS middleware

#### Proof of Concept
```bash
curl -s -I -H "Origin: https://evil.com" https://api.company.com/orders
# HTTP/1.1 200 OK
# Access-Control-Allow-Origin: *
# Access-Control-Allow-Credentials: true
```

#### Impact
Any website can read API responses on behalf of authenticated users.

#### Remediation
Restrict CORS to trusted origins and never combine wildcard origins with credentials.

```python
# Fixed: explicit origin allowlist
ALLOWED_ORIGINS = {"https://app.company.com", "https://admin.company.com"}

@app.middleware("http")
async def cors_middleware(request, call_next):
    origin = request.headers.get("Origin")
    response = await call_next(request)
    if origin in ALLOWED_ORIGINS:
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Credentials"] = "true"
    return response
```

#### References
- OWASP A05:2021: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CORS spec: https://fetch.spec.whatwg.org/#cors-protocol

## Remediation Tracking

| ID | Finding | Owner | Due Date | Status |
|----|---------|-------|----------|--------|
| 001 | SQL Injection in orders endpoint | Backend team | +2 days | In progress |
| 002 | Missing rate limiting on login | Platform team | +7 days | Remediated |
| 003 | CORS misconfiguration | Platform team | +7 days | Remediated |
| 004 | Verbose error messages | Backend team | +14 days | Remediated |
| 005 | Missing security headers | DevOps team | +14 days | Remediated |
| 006 | JWT in URL query parameter | Backend team | +30 days | Open |
| 007 | Outdated TLS 1.0 support | DevOps team | +30 days | Remediated |
| 008 | Debug endpoints exposed in production | DevOps team | +14 days | Remediated |
| 009 | No account lockout policy | Backend team | +30 days | Open |
| 010 | Session token in localStorage | Frontend team | +90 days | Open |

## Risk Rating Matrix

| Likelihood \ Impact | Low | Medium | High |
|---------------------|-----|--------|------|
| High | Medium | High | Critical |
| Medium | Low | Medium | High |
| Low | Info | Low | Medium |

## Methodology

- OWASP Testing Guide v4.2
- OWASP API Security Top 10 (2023)
- PTES (Penetration Testing Execution Standard)

## Tools Used

- Burp Suite Professional 2024.2
- OWASP ZAP 2.14
- Nmap 7.94
- Semgrep 1.52 (source code review)
- Custom Python scripts for API fuzzing

## Sign-off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Lead tester | [name] | 2026-08-19 | [signature] |
| Engineering lead | [name] | 2026-08-20 | [signature] |
| Security officer | [name] | 2026-08-20 | [signature] |
