# Post-Deployment Verification: payments-api v3.2.1

## Deployment Info
| Field | Value |
|-------|-------|
| **Deployer** | Jane Doe |
| **Timestamp** | 2026-07-15 14:30 UTC |
| **Environment** | production |
| **Rollback commit** | a1b2c3d4e5f6 |

## Health Checks

- [x] Application starts without errors
- [x] Health endpoint returns 200: `GET /health`
- [x] Readiness probe passes
- [x] Liveness probe passes
- [x] Database connectivity confirmed
- [x] External dependency connectivity confirmed (Stripe, PayPal)

## Smoke Tests

- [x] Core user flow: login → create order → checkout → logout
- [x] API returns expected status codes (200, 201, 400, 401, 500)
- [x] Critical path: credit card payment flow
- [x] Admin dashboard loads with new metrics

## Metrics Validation

| Metric | Pre-Deploy | Post-Deploy | Delta | Alert? |
|--------|-----------|-------------|-------|--------|
| Error rate | 0.05% | 0.04% | -0.01% | No |
| Latency p95 | 120ms | 118ms | -2ms | No |
| CPU usage | 45% | 48% | +3% | No |
| Memory | 512MB | 520MB | +8MB | No |
| Throughput | 850 req/s | 860 req/s | +10 | No |

## Security & Logs

- [x] Security headers present (`curl -I https://api.example.com` → CSP + HSTS)
- [x] TLS certificate valid until 2027-01-20
- [x] 401/403 rate unchanged (0.8% pre, 0.7% post)
- [x] No new exception patterns (checked `payments-api` error log)
- [x] No secrets in logs

## Rollback Readiness

- [x] Rollback script tested in last 30 days
- [x] Previous version artifacts available (v3.2.0)
- [x] Database migration is backward-compatible
- [x] Feature flags can disable new code instantly

## Sign-Off

| Role | Name | Time |
|------|------|------|
| Deployer | Jane Doe | 14:35 UTC |
| On-call | Bob Smith | 14:40 UTC |
