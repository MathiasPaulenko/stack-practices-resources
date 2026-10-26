# Access Control Policy — `<Organization Name>`

## Policy Overview

| Field | Value |
|-------|-------|
| Organization | Example Corp |
| Policy Version | 2.0 |
| Last Updated | 2026-07-05 |
| Policy Owner | CISO |
| Approved By | Executive Committee |
| Review Cycle | Annual |
| Next Review | 2027-07-05 |
| Compliance Frameworks | SOC 2, ISO 27001, HIPAA |
| Access Model | RBAC + ABAC (hybrid) |

## 1. Authentication

### Authentication Methods

| Method | Use Case | MFA Required | Notes |
|--------|----------|--------------|-------|
| Password + MFA | User login (all) | Yes (TOTP or hardware key) | Default for all users |
| SSO (SAML/OIDC) | Enterprise apps | Yes (via IdP) | Okta as IdP |
| API keys | Service-to-service | N/A | Rotated every 90 days |
| OAuth 2.0 | Third-party integrations | N/A | Scoped tokens, 1-hour expiry |
| SSH keys | Server access | Yes (MFA on jump host) | Ed25519 keys only |
| Client certificates | mTLS services | N/A | Issued by internal CA |

### Password Policy

| Requirement | Value | Rationale |
|-------------|-------|-----------|
| Minimum length | 14 characters | Resistance to brute force |
| Character classes | 3 of 4 (upper, lower, digit, special) | Complexity without complexity rules |
| Password history | Last 24 passwords | Prevent reuse |
| Password age | No maximum (NIST guidance) | Frequent changes cause weaker passwords |
| Breach check | Check against Have I Been Pwned | Prevent use of breached passwords |
| Lockout threshold | 10 failed attempts | Account lockout after 10 tries |
| Lockout duration | 15 minutes | Auto-unlock after 15 min |
| Storage | Argon2id hash | Memory-hard, slow cracking |

### Multi-Factor Authentication (MFA)

| User Group | MFA Method | Enforcement | Recovery |
|-------------|------------|-------------|----------|
| All employees | TOTP (Google Authenticator) | Required at login | Backup codes |
| Administrators | Hardware key (YubiKey) | Required at login | Backup hardware key |
| Developers | TOTP or hardware key | Required for prod access | Backup codes |
| Service accounts | No MFA (API key) | N/A | Key rotation |
| Contractors | TOTP | Required at login | Sponsor-managed |

### MFA Enrollment Process

| Step | Action | Responsible | Duration |
|------|--------|-------------|----------|
| 1 | User requests MFA enrollment | User | — |
| 2 | IT verifies identity | IT Support | 1 business day |
| 3 | User installs authenticator app | User | 15 minutes |
| 4 | User scans QR code | User + IT | 5 minutes |
| 5 | User verifies with test code | User | 2 minutes |
| 6 | User saves backup codes | User | 5 minutes |
| 7 | IT enables MFA enforcement | IT Support | Same day |

## 2. Authorization

### Role-Based Access Control (RBAC)

| Role | Description | Permissions | Assignment |
|------|-------------|-------------|------------|
| Viewer | Read-only access | View dashboards, reports | Auto-assigned to all employees |
| Developer | Development access | Code repos, CI/CD, staging | Manager approval |
| Senior Developer | Development + review | Code repos, CI/CD, staging, prod read | Manager + tech lead approval |
| DevOps Engineer | Infrastructure access | All infrastructure, prod deploy | Manager + CISO approval |
| Administrator | Full system access | All systems, user management | Manager + CISO + CEO approval |
| Auditor | Read-only audit access | Access logs, audit reports | CISO approval |
| Service Account | Automated access | Specific API endpoints | Technical owner approval |

### Permission Matrix

| Resource | Viewer | Developer | Senior Dev | DevOps | Admin | Auditor |
|----------|--------|-----------|------------|--------|-------|---------|
| Dashboards | ✅ Read | ✅ Read | ✅ Read | ✅ Read | ✅ Read | ✅ Read |
| Code repos | ❌ | ✅ Read/Write | ✅ Read/Write | ✅ Read | ✅ Read/Write | ✅ Read |
| CI/CD pipelines | ❌ | ✅ Trigger | ✅ Trigger | ✅ Configure | ✅ Configure | ✅ Read |
| Staging environment | ❌ | ✅ Deploy | ✅ Deploy | ✅ Deploy | ✅ Deploy | ✅ Read |
| Production environment | ❌ | ❌ | ✅ Read | ✅ Deploy | ✅ Deploy | ✅ Read |
| User management | ❌ | ❌ | ❌ | ❌ | ✅ Manage | ✅ Read |
| Audit logs | ❌ | ❌ | ❌ | ✅ Read | ✅ Read | ✅ Read |
| Security settings | ❌ | ❌ | ❌ | ✅ Read | ✅ Manage | ✅ Read |

### Attribute-Based Access Control (ABAC)

| Attribute | Values | Effect on Access |
|-----------|--------|------------------|
| Department | Engineering, Finance, HR, Sales | Restricts to department resources |
| Location | Office, Remote, VPN | Remote requires VPN for prod |
| Time | Business hours, Off-hours | Prod deploy only in business hours |
| Device | Managed, Unmanaged | Unmanaged devices blocked from prod |
| Risk score | Low, Medium, High | High risk requires step-up auth |

### Privileged Access Management (PAM)

| Privilege | Access Method | Approval | Duration | Logging |
|-----------|--------------|----------|----------|---------|
| Production SSH | Jump host with MFA | Manager approval | 4 hours | Full session recording |
| Database admin | Bastion with MFA | Manager + DBA approval | 2 hours | Query logging |
| Cloud console | Break-glass account | CISO approval | 1 hour | Full audit trail |
| Kubernetes admin | kubectl via jump host | Manager approval | 4 hours | Command logging |
| Root/sudo | Just-in-time elevation | Manager + CISO approval | 1 hour | Command logging |

## 3. Session Management

### Session Configuration

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Session timeout (active) | 8 hours | Workday without re-auth |
| Session timeout (idle) | 30 minutes | Auto-logout on inactivity |
| Session timeout (privileged) | 1 hour | Shorter for admin sessions |
| Concurrent sessions | 3 max | Prevent session sharing |
| Session storage | HTTP-only, Secure cookies | Prevent XSS theft |
| CSRF protection | SameSite=Strict cookies | Prevent CSRF attacks |
| Session invalidation | On password change | Force re-auth after change |
| Token expiry (API) | 1 hour access, 30 days refresh | Short-lived access tokens |

### Session Security

| Check | Implementation | Verification |
|-------|----------------|--------------|
| Tokens signed | JWT with RS256 | Verify signature on every request |
| Tokens encrypted | JWE for sensitive claims | Decrypt server-side only |
| Refresh token rotation | New refresh token each use | Detect token theft |
| Device binding | Token bound to device fingerprint | Reject from other devices |
| IP binding | Token bound to IP range | Reject from unexpected IPs |
| Session revocation | Revocation list checked | Immediate logout |

## 4. Access Provisioning

### Onboarding Process

| Step | Action | Responsible | SLA |
|------|--------|-------------|-----|
| 1 | HR creates employee record | HR | Before start date |
| 2 | IT creates accounts | IT | 1 business day |
| 3 | Manager requests access | Manager | 1 business day |
| 4 | Access approved | Data Owner | 2 business days |
| 5 | Access provisioned | IT | 1 business day |
| 6 | User notified | IT | Same day |
| 7 | Access recorded | Compliance | 1 business day |

### Offboarding Process

| Step | Action | Responsible | SLA |
|------|--------|-------------|-----|
| 1 | HR notifies departure | HR | On departure date |
| 2 | Manager confirms last day | Manager | Same day |
| 3 | Access revoked | IT | Within 24 hours |
| 4 | Devices returned | IT | Within 3 days |
| 5 | Accounts deactivated | IT | Within 24 hours |
| 6 | Access recorded | Compliance | 1 business day |
| 7 | Final access review | Compliance | 1 week |

### Access Change Process

| Trigger | Action | Approver | SLA |
|---------|--------|----------|-----|
| Role change | Review and update access | New manager | 3 business days |
| Team transfer | Remove old team access, add new | New manager | 3 business days |
| Promotion | Add new role permissions | Manager + CISO | 5 business days |
| Demotion | Remove elevated access | Manager | 1 business day |
| Temporary access | Grant with expiry date | Manager + Data Owner | 1 business day |

## 5. Access Reviews

### Review Schedule

| Scope | Frequency | Reviewer | Action |
|-------|-----------|----------|--------|
| All user access | Quarterly | Manager | Remove unused access |
| Privileged access | Monthly | CISO | Verify need-to-know |
| Service accounts | Quarterly | Technical Owner | Verify still needed |
| External access | Monthly | Sponsor | Verify contract active |
| Dormant accounts | Monthly | IT | Disable after 30 days inactive |
| Orphaned accounts | Monthly | IT | Remove accounts with no owner |

### Review Checklist

| Check | Method | Pass Criteria |
|-------|--------|---------------|
| User still employed | Cross-reference with HR | All users have active HR record |
| Access matches role | Compare permissions to role definition | No excessive permissions |
| No shared accounts | Verify unique user per account | Each account has one user |
| MFA enabled | Check IdP MFA enrollment | 100% enrollment |
| No dormant accounts | Check last login date | No accounts inactive > 30 days |
| Service accounts documented | Check service account registry | All accounts have owner and purpose |
| Temporary access expired | Check expiry dates | No expired temporary access |

## 6. API and Service Access

### API Authentication

| API Type | Authentication | Token Lifetime | Scope | Rate Limit |
|----------|---------------|----------------|-------|------------|
| Public API | OAuth 2.0 (PKCE) | 1 hour access | Per-client scope | 1000 req/min |
| Internal API | mTLS | Certificate lifetime | Service identity | 5000 req/min |
| Service-to-service | JWT (RS256) | 1 hour | Service scope | 10000 req/min |
| Webhook | HMAC signature | Per-request | N/A | 100 req/min |
| Admin API | API key + MFA | 90 days rotation | Admin scope | 100 req/min |

### API Key Management

| Requirement | Implementation | Verification |
|-------------|----------------|--------------|
| Key generation | Cryptographically random, 256-bit | Verify entropy |
| Key storage | Hashed at rest (bcrypt) | Verify hash, not plaintext |
| Key transmission | TLS 1.2+ only | Verify no HTTP |
| Key rotation | Every 90 days | Automated rotation pipeline |
| Key revocation | Immediate via revocation list | Verify revocation propagation |
| Key scope | Least privilege per key | Audit scopes quarterly |
| Key logging | Never log key values | Grep logs for key patterns |
