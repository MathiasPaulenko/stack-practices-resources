# Secrets Rotation Schedule

## 1. Secret Inventory

| Secret | Type | Environment | Storage Location | Current Version | Last Rotated | Next Rotation | Owner |
|--------|------|-------------|------------------|-----------------|--------------|---------------|-------|
| | | | | | | | |

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

1. Generate new secret in Vault / secrets manager
2. Deploy application with dual-read: app accepts both old and new secret
3. Validate: confirm new secret works in staging
4. Update consumers: rotate downstream services one by one
5. Remove old secret: after validation period (24–48 hours)
6. Update inventory: mark new version and date

### Certificate Rotation (TLS)

1. Provision new certificate from CA
2. Deploy to load balancer / ingress alongside existing certificate
3. Validate: SSL Labs scan + synthetic monitor
4. Wait for propagation: ensure all edge caches refreshed
5. Remove old certificate from all endpoints
6. Update inventory: mark new expiry date

## 4. Emergency Rotation Playbook

| Trigger | Action | Owner | SLA |
|---------|--------|-------|-----|
| Secret exposed in public repo | Rotate immediately; revoke old | @security-owner | 1 hour |
| Employee with secret access terminated | Rotate all secrets they had access to | @security-owner + @owner | 4 hours |
| Suspected breach | Rotate all critical secrets; incident response | @security-owner | 24 hours |
| Certificate expires in < 7 days | Emergency reissue + deploy | @infra-owner | 24 hours |

## 5. Validation Checklist

- [ ] New secret is readable by all expected services
- [ ] Old secret is revoked / deleted (not just unused)
- [ ] Application logs show no authentication failures post-rotation
- [ ] CI/CD pipelines pass with new secret
- [ ] Monitoring alerts are green for 24 hours
- [ ] Inventory updated with new version and rotation date
- [ ] Runbook updated if procedure changed

## 6. Exception Log

| Secret | Reason for Extended Interval | Risk Accepted By | New Date | Review |
|--------|------------------------------|------------------|----------|--------|
| | | | | |

## 7. Rotation Metrics

| Month | Secrets Scheduled | Rotated On Time | Late | Compliance Rate |
|-------|------------------:|----------------:|-----:|----------------:|
| | | | | |
