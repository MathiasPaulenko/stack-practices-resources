# Secret Rotation Schedule

> Companion file for the [Secret Rotation Schedule Template](https://stackpractices.com/docs/secret-rotation-schedule-template/) on StackPractices.
> Fill every `YYYY-MM-DD`, `@owner`, and blank cell before relying on this schedule.

## 1. Secret Inventory

| Secret | Type | Environment | Storage Location | Current Version | Last Rotated | Next Rotation | Owner |
|--------|------|-------------|------------------|-----------------|--------------|---------------|-------|
| `DB_MASTER_PASSWORD` | Password | Production | HashiCorp Vault | `v3` | `YYYY-MM-DD` | `YYYY-MM-DD` | @db-owner |
| `AWS_ACCESS_KEY_ID` | API key | Production | AWS Secrets Manager | `v2` | `YYYY-MM-DD` | `YYYY-MM-DD` | @infra-owner |
| `JWT_SIGNING_KEY` | Signing key | All | Vault / HSM | `v4` | `YYYY-MM-DD` | `YYYY-MM-DD` | @security-owner |
| `TLS_CERT_API` | Certificate | Production | Cert-manager + Vault | `v2` | `YYYY-MM-DD` | `YYYY-MM-DD` | @infra-owner |
| `GITHUB_DEPLOY_TOKEN` | Token | CI/CD | GitHub Secrets | `v1` | `YYYY-MM-DD` | `YYYY-MM-DD` | @devops-owner |

## 2. Rotation Cadence Policy

| Secret Type | Rotation Interval | Trigger Events | Grace Period |
|-------------|-------------------|----------------|--------------|
| Database passwords | 90 days | Employee departure, suspected breach | 7 days |
| Cloud API keys | 90 days | Key exposed in logs, IAM policy change | 7 days |
| TLS certificates | Auto-renew (30 days before expiry) | Certificate expiry alert | 14 days |
| Signing / encryption keys | 180 days | Key compromise, algorithm deprecation | 14 days |
| CI/CD tokens | 90 days | Token scope change, repository access change | 3 days |
| Service account passwords | 90 days | Role change, service decommission | 7 days |
| Emergency break-glass | Per-use | After each use | Immediate |

Alert at 30, 14, and 7 days before each due date.

## 3. Rotation Procedure

### Zero-Downtime Key Rotation (Application Secrets)

1. Generate new secret in Vault / secrets manager.
2. Deploy application with dual-read: app accepts both old and new secret.
3. Validate the new secret works in staging.
4. Update consumers one by one.
5. Remove the old secret after the validation window (24–48 hours).
6. Update the inventory with the new version and date.

### Certificate Rotation (TLS)

1. Provision new certificate from the CA.
2. Deploy to load balancer / ingress alongside the existing certificate.
3. Validate with an SSL scan and a synthetic monitor.
4. Wait for propagation through every edge cache.
5. Remove the old certificate from all endpoints.
6. Update the inventory with the new expiry date.

## 4. Emergency Rotation Playbook

| Trigger | Action | Owner | SLA |
|---------|--------|-------|-----|
| Secret exposed in public repo | Rotate immediately; revoke old | @security-owner | 1 hour |
| Employee with secret access terminated | Rotate all secrets they had access to | @security-owner + @owner | 4 hours |
| Suspected breach | Rotate all critical secrets; incident response | @security-owner | 24 hours |
| Certificate expires in < 7 days | Emergency reissue + deploy | @infra-owner | 24 hours |

## 5. Escalation for Overdue Rotations

| Condition | Action | Escalation Target | Timeline |
|-----------|--------|-------------------|----------|
| Secret overdue by 7 days | Notify owner and manager | Engineering manager | Immediate |
| Secret overdue by 30 days | Escalate to security review | Security team | Within 48 hours |
| Rotation failed twice | Roll back, review procedure | Platform lead | Same day |

## 6. Validation Checklist

- [ ] New secret is readable by all expected services
- [ ] Old secret is revoked / deleted (not just unused)
- [ ] Application logs show no authentication failures post-rotation
- [ ] CI/CD pipelines pass with the new secret
- [ ] Monitoring alerts are green for 24 hours
- [ ] Inventory updated with new version and rotation date
- [ ] Runbook updated if the procedure changed

## 7. Exception and Risk Acceptance Log

| Secret | Reason for Extended Interval | Compensating Control | Risk Accepted By | Review Date |
|--------|------------------------------|----------------------|------------------|-------------|
| `LEGACY_SFTP_KEY` | Legacy system can't do dual-read | Manual rotation with approval; access limited to VPC | @ciso | `YYYY-MM-DD` |
| | | | | |

## 8. Rotation Metrics

| Month | Secrets Scheduled | Rotated On Time | Late | Compliance Rate |
|-------|------------------:|----------------:|-----:|----------------:|
| | | | | |
