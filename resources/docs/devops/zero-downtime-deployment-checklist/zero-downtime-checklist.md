# Zero-Downtime Deployment Checklist

Release: `<version>` · Service: `<service-name>` · Date: `<YYYY-MM-DD>` · Deployer: `<name>` · On-call: `<name>`

Work through the seven phases in order — each assumes the previous one passed. Every unchecked box is a deliberate decision you should be able to defend in a postmortem.

## 1. Pre-Deployment Readiness

- [ ] The change is approved and documented, with a named deployer and on-call owner.
- [ ] Code is merged and the artifact is built, tagged, and immutable.
- [ ] Unit, integration, and contract tests pass in CI.
- [ ] Database migrations were reviewed for backward compatibility.
- [ ] Feature flags are configured so new behavior can be toggled off without redeploying.
- [ ] Capacity covers the expected traffic plus the surge from duplicated instances during rollout.
- [ ] Dashboards and alerts are live and linked in the release ticket.
- [ ] The on-call rotation knows the deployment window and the escalation path.
- [ ] Rollback steps were tested in staging within the last quarter, not just written down.
- [ ] Customer-facing communication is drafted if the change is user-visible.

## 2. Health Check Configuration

| Check | Endpoint | Success Criteria | Failure Action |
|-------|----------|------------------|----------------|
| Liveness | `/health/live` | HTTP 200 | Restart container |
| Readiness | `/health/ready` | HTTP 200 and dependencies reachable | Stop traffic routing |
| Startup | `/health/startup` | HTTP 200 | Delay rollout |
| Dependency | `/health/deps` | Database, cache, and queue respond | Alert and halt |
| Business | `/health/business` | Critical flow returns expected value | Page on-call |

## 3. Rollout Strategy Selection

| Strategy | Use Case | Risk Level | Rollback Speed |
|----------|----------|------------|----------------|
| Rolling update | Stateless services, low risk | Low | Medium (terminate new pods) |
| Blue-green | Stateful sessions, predictable releases | Medium | Fast (switch traffic back) |
| Canary | High risk, measurable metrics | Medium | Fast (drain canary) |
| Feature flag | Gradual user exposure | Low | Instant (toggle off) |
| A/B deployment | Validate user behavior | Medium | Fast (re-route traffic) |

Selected strategy: `<strategy>` · Reason: `<why>` · Fallback: `<alternative>`

## 4. Deployment Execution Steps

| Step | Action | Verification |
|------|--------|--------------|
| 1 | Deploy to staging and run smoke tests | Staging tests pass |
| 2 | Deploy canary or a small subset | Health checks pass, error rate stable |
| 3 | Monitor key metrics for the canary duration | Latency, error rate, business metrics within baseline |
| 4 | Increase traffic percentage gradually | Each stage passes health and metric checks |
| 5 | Complete rollout to 100% | All instances healthy and serving traffic |
| 6 | Validate production endpoints | Smoke tests and critical user flows pass |
| 7 | Keep the old version available for rollback | Retain for the defined rollback window |
| 8 | Confirm the rollback window has passed | Remove old version or update the artifact baseline |

## 5. Database Migration Safety

- [ ] Migrations are additive and work with the previous application version.
- [ ] Old code can read the new schema without errors.
- [ ] New code can read the old schema if a rollback is needed.
- [ ] Indexes are created concurrently where the engine supports it.
- [ ] Large migrations are split into batches small enough to stay under lock timeouts.
- [ ] Backfill and migration jobs are idempotent and resumable.
- [ ] A rollback script or compensating operation exists and was tested.
- [ ] Schema changes were tested in staging against production-like data volume.

## 6. Rollback Triggers

| Trigger | Threshold | Action |
|---------|-----------|--------|
| Error rate spike | > 0.5% for 2 minutes | Pause rollout and investigate |
| Latency increase | p99 > baseline + 30% for 5 minutes | Roll back traffic |
| Business metric drop | Conversion rate drops > 5% | Roll back immediately |
| Health check failure | > 10% of instances failing | Roll back immediately |
| Critical alert | Any P1 incident | Roll back and page on-call |
| Canary timeout | Canary stage exceeds its duration without passing | Roll back the canary |

Adjust thresholds to your SLOs before the release — don't copy them blindly.

## 7. Post-Deployment Validation

- [ ] Application logs show no unexpected errors or new exception types.
- [ ] Error rate and latency sit within baseline for at least 30 minutes.
- [ ] Business metrics are stable or improving.
- [ ] Feature flags are in their intended state.
- [ ] Old resources stay available until the rollback window closes, then get cleaned up.
- [ ] A deployment summary goes out to the team with links to dashboards.
- [ ] Any issues found are logged in the tracker with owners.

## Sign-off

Deployer: `<name>` · On-call: `<name>` · Outcome: `<success | rolled back>` · Notes: `<what deviated>`
