# Post-Deployment Verification: [Service] v[X.Y.Z]

## Deployment Info
| Field | Value |
|-------|-------|
| **Deployer** | [name] |
| **Timestamp** | [YYYY-MM-DD HH:MM UTC] |
| **Environment** | [staging / production] |
| **Rollback commit** | [SHA] |

## Health Checks

- [ ] Application starts without errors
- [ ] Health endpoint returns 200: `GET /health`
- [ ] Readiness probe passes
- [ ] Liveness probe passes
- [ ] Database connectivity confirmed
- [ ] External dependency connectivity confirmed

## Smoke Tests

- [ ] Core user flow: [login → action → logout]
- [ ] API returns expected status codes
- [ ] Critical path payment flow
- [ ] Admin dashboard loads

## Metrics Validation

| Metric | Pre-Deploy | Post-Deploy | Delta | Alert? |
|--------|-----------|-------------|-------|--------|
| Error rate | 0.05% | ___ | ___ | ___ |
| Latency p95 | 120ms | ___ | ___ | ___ |
| CPU usage | 45% | ___ | ___ | ___ |

## Security & Logs

- [ ] Security headers present on key routes (`curl -I` shows CSP, HSTS)
- [ ] TLS certificate valid, expiry > 30 days
- [ ] No spike in 401/403 responses vs pre-deploy baseline
- [ ] No new exception patterns in application logs
- [ ] No secrets or credentials leaked in logs

## Rollback Readiness

- [ ] Rollback script tested in last 30 days
- [ ] Previous version artifacts available
- [ ] Database migration is backward-compatible
- [ ] Feature flags can disable new code instantly

## Sign-Off

| Role | Name | Time |
|------|------|------|
| Deployer | | |
| On-call | | |
