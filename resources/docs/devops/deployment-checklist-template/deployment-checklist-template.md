# Deployment Checklist: `<Release Name>`

## Release Metadata

| Field | Value |
|-------|-------|
| Service | `name` |
| Version | `x.y.z` |
| Branch / Commit | `main@abc1234` |
| Deployer | `@username` |
| Date | `YYYY-MM-DD HH:MM UTC` |
| Ticket / PR | `PROJ-123` |

## 1. Pre-Deployment

### 1.1. Code & Tests

- [ ] All CI checks pass (lint, unit tests, integration tests)
- [ ] Code review approved by at least one senior engineer
- [ ] No unresolved security alerts (Snyk, Dependabot)
- [ ] Database migrations reviewed for backward compatibility
- [ ] Feature flags configured and defaulted to off

### 1.2. Infrastructure

- [ ] Staging environment deployed and validated
- [ ] Production capacity verified (CPU, memory, disk)
- [ ] Autoscaling rules reviewed (min / max replicas)
- [ ] Rollback artifact built and stored (Docker image, AMI)
- [ ] CDN cache invalidation plan documented (if applicable)

### 1.3. Communication

- [ ] Stakeholders notified of deployment window
- [ ] On-call engineer aware and available
- [ ] Status page updated to "Maintenance" (if downtime expected)
- [ ] Customer-facing teams briefed on changes

## 2. Deployment

### 2.1. Database (if applicable)

- [ ] Migration scripts tested against a copy of production data
- [ ] Migration run with `ALTER TABLE ... ADD COLUMN` (not destructive ops first)
- [ ] Migration duration estimated and approved by DBA
- [ ] Rollback script prepared for destructive changes

### 2.2. Application

- [ ] Deploy using blue/green or canary strategy
- [ ] Monitor error rate for 5 minutes after each canary increment
- [ ] Verify health checks return 200 OK
- [ ] Confirm new pods/containers are receiving traffic

### 2.3. Verification

- [ ] Smoke tests pass against production endpoints
- [ ] Critical user journeys tested (login, checkout, search)
- [ ] Logs show no unexpected errors or exceptions
- [ ] Metrics within baseline (latency p95, error rate, CPU)

## 3. Post-Deployment

### 3.1. Validation

- [ ] Feature flags enabled incrementally (5% → 25% → 100%)
- [ ] A/B test results monitored (if applicable)
- [ ] Customer support briefed on new capabilities or changes
- [ ] Documentation updated (API docs, runbooks, wiki)

### 3.2. Monitoring

- [ ] Dashboards checked for anomalies (traffic, errors, latency)
- [ ] Alerts firing as expected (no false positives or muted alerts)
- [ ] Synthetic monitoring passes (Pingdom, Datadog Synthetics)
- [ ] Error tracking reviewed (Sentry, Rollbar) for new issues

### 3.3. Cleanup

- [ ] Old versions scaled down after stability confirmed (30 min)
- [ ] Feature branches deleted
- [ ] Deployment log archived for audit
- [ ] Status page updated to "Operational"
