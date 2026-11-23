# Patch Management Plan: `<System / Service>`

## 1. Patch Inventory

| CVE / Advisory | Severity | CVSS | Affected Systems | Patch Available | Current Version | Target Version | Owner |
|----------------|----------|------|------------------|-----------------|-----------------|----------------|-------|
| CVE-YYYY-NNNNN | Critical | 9.8 | `list` | `YYYY-MM-DD` | `X.Y.Z` | `A.B.C` | `@sre-team` |
| GHSA-YYYY-NNNNN | High | 7.5 | `list` | `YYYY-MM-DD` | `X.Y.Z` | `A.B.C` | `@platform-team` |

## 2. Patch Classification

| Severity | Criteria | Test Requirement | Deployment Window | SLA |
|----------|----------|------------------|-------------------|-----|
| Critical | RCE, privilege escalation, data exfiltration; actively exploited | Minimal: smoke test in staging | Emergency: within 24 hours | 24 hours |
| High | Remote attack vector; no known exploit yet | Standard: full regression in staging | Next maintenance window | 7 days |
| Medium | Local access required; complex exploit chain | Standard: full regression in staging | Next maintenance window | 30 days |
| Low | Denial of service only; no data impact | Deferred: test with next release | Next release cycle | 90 days |

## 3. Testing Checklist

- [ ] Patch applies cleanly without manual intervention
- [ ] Application starts successfully after patch
- [ ] Core user journeys pass (smoke test)
- [ ] Integration tests pass against patched environment
- [ ] Performance benchmarks within 5% of baseline
- [ ] No new errors in logs during 30-minute soak test
- [ ] Rollback image / snapshot available before production deploy

## 4. Deployment Schedule

| Environment | Window | Pre-approval Required | Rollback Ready |
|-------------|--------|----------------------|----------------|
| Staging | Anytime | Team lead sign-off | Previous image tagged |
| Canary (5% traffic) | Low-traffic hours | Manager notification | Instant rollback via LB |
| Production — Batch A (non-critical) | Tuesday 10:00 UTC | CAB for Critical patches | Snapshot + runbook tested |
| Production — Batch B (critical) | Immediate after staging pass | Security + manager | Snapshot + runbook tested |

## 5. Verification

| Check | Method | Owner | Timeline |
|-------|--------|-------|----------|
| Vulnerability scan post-patch | Nessus / Trivy / Snyk | `@security-team` | Within 24 hours of deploy |
| System health metrics | Grafana / Datadog dashboard | `@sre-team` | 1 hour post-deploy |
| Error rate baseline comparison | APM tool | `@sre-team` | 4 hours post-deploy |
| User-facing functional test | Synthetic monitoring | `@qa-team` | 4 hours post-deploy |
| Dependency audit | `npm audit`, `pip-audit`, OS package manager | `@platform-team` | Weekly |

## 6. Exception Log

| CVE | Reason for Delay | Risk Accepted By | Expiry Date | Compensating Control |
|-----|------------------|------------------|-------------|----------------------|
| | | | | |
