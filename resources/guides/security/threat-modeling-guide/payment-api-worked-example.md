# Worked Example: Payment API

```text
System: Payment API, OAuth2, handles credit cards
Method: STRIDE per element + risk matrix

Flow:
  Client -> API Gateway -> Auth Service -> Payment Service
                                    -> Vault (secrets)
                                    -> DB (transactions)
                                    -> Stripe API

Identified threats:
  | Category | Threat                          | Mitigation                      | Severity |
  |----------|---------------------------------|---------------------------------|----------|
  | Spoofing | Forged JWT token                | Verify signature + expiry       | High     |
  | Spoofing | Client impersonates another user| Scope validation per user       | High     |
  | Tampering| Modify amount in request        | HMAC signature on payload       | High     |
  | Tampering| Man-in-the-middle               | TLS 1.3 + certificate pinning   | Medium   |
  | Repudiation | User denies transaction     | Immutable audit log + timestamp | High     |
  | Info Disclosure | Card number in logs    | Masking + PCI DSS compliance    | Critical |
  | Info Disclosure | Error exposes stack trace | Generic messages in prod    | Medium   |
  | DoS      | Request flood                   | Rate limiting + WAF             | High     |
  | DoS      | Expensive query without limit   | Pagination + query timeout      | Medium   |
  | EoP      | Regular user accesses admin     | RBAC + scope validation         | High     |
  | EoP      | Service account over-permissioned | Least privilege + IAM audit   | High     |

Prioritization (risk = impact x likelihood):
  | Threat                  | Impact | Likelihood | Risk | Priority |
  |-------------------------|--------|------------|------|----------|
  | Forged JWT              | 5      | 4          | 20   | 1        |
  | Card logging            | 5      | 3          | 15   | 1        |
  | Missing rate limiting   | 4      | 4          | 16   | 1        |
  | Amount modification     | 4      | 3          | 12   | 2        |
  | Stack trace exposed     | 3      | 4          | 12   | 3        |
  | Missing RBAC            | 5      | 2          | 10   | 3        |

Mitigation plan:
  1. JWT verification: signature + expiry + issuer
  2. Per-user scope validation in every handler
  3. Sign critical payloads with HMAC (amount, destination account)
  4. Cap request rates: 100/min per user, 1000/min per IP
  5. Three roles (user, admin, super_admin), each scoped per resource
  6. Append-only audit log, hash-chained so tampering shows
  7. Generic error messages; stack traces stay in logs
  8. WAF: OWASP rules + custom rules for payment endpoints
```
