# Incident Timeline: `auth-service login latency (JWT secret rotation)`

## Metadata

| Field | Value |
|-------|-------|
| Incident ID | INC-2026-07-11-001 |
| Severity | SEV1 |
| Date | 2026-07-11 |
| Service(s) Affected | auth-service |
| Incident Commander | On-call engineer |
| Timeline Author | Scribe |

## Summary

| Metric | Value |
|--------|-------|
| Time to Detect (TTD) | 13 min |
| Time to Acknowledge (TTA) | 2 min |
| Time to Mitigate (TTM) | 17 min |
| Time to Resolve (TTR) | 30 min |
| Total Customer Impact Duration | ~17 min (15% → <0.5% error rate) |

## Detailed Timeline

| Time (UTC) | Event | Source | Actor | Notes |
|------------|-------|--------|-------|-------|
| 10:40 | Config deploy: JWT secret rotation interval | CI/CD logs | deploy-bot | |
| 10:42 | DB CPU begins rising | CloudWatch | System | Baseline ~40% |
| 10:50 | DB CPU hits 95% (threshold 80%) | CloudWatch | System | **Alert expected here — none fired** |
| 10:52 | Login latency p99 > 2s (threshold 1s) | APM | System | |
| 10:55 | PagerDuty alert: auth-service latency critical | PagerDuty | System | Detection gap: 13 min |
| 10:55 | PagerDuty alert: DB CPU critical | PagerDuty | System | |
| 10:57 | On-call acknowledges both alerts | PagerDuty | On-call | |
| 10:58 | Opens #inc-2026-07-11 | Slack | On-call | |
| 11:00 | SEV1 declared — 15% of logins failing | Slack | On-call | |
| 11:01 | Checks recent deploys — config deploy at 10:40 | CI/CD | On-call | |
| 11:03 | Identifies change: JWT secret rotation interval | Git history | On-call | |
| 11:04 | Notifies #support | Slack | On-call | |
| 11:05 | Initiates config rollback | CI/CD | On-call | |
| 11:08 | Rollback deployed | CI/CD | System | |
| 11:08 | Error rate: 15% → 8% → 3% | Monitoring | On-call | |
| 11:12 | Error rate < 0.5%; status page updated | Monitoring | On-call | Mitigated |
| 11:15 | 10-min stability window | Dashboards | On-call | Deliberate |
| 11:25 | Incident resolved; status page updated | Slack | On-call | |

## Delay Analysis

| Gap | Duration | Root Cause | Action Item |
|-----|----------|------------|-------------|
| Detection (10:42→10:55) | 13 min | DB CPU alert threshold too high; no latency alert | IMPROVE-1: lower DB CPU threshold to 80%, add p99 latency alert |
| Alert → Acknowledge | 2 min | — | Good |
| Acknowledge → Declaration | 3 min | — | Good |
| Declaration → Root cause | 4 min | Checked recent deploys first | Good — document as practice |
| Root cause → Mitigation | 3 min | Fast rollback path | Good |
| Mitigation → Resolution | 10 min | Standard stability window | Acceptable |

## What Went Well

1. On-call checked recent deploys immediately — root cause in 4 min
2. Status page updated proactively at mitigation
3. Both alerts acknowledged together, no delay

## What Went Poorly

1. 13-minute detection gap: DB CPU climbed for 13 min before any alert
2. Config change had no canary or staged rollout
3. No automated link between deploy events and alerts

## Action Items

| ID | Action | Owner | Due Date | Priority |
|----|--------|-------|----------|----------|
| IMPROVE-1 | Lower DB CPU alert to 80% + add p99 latency alert | Platform | 2026-07-18 | High |
| IMPROVE-2 | Require canary stage for config deploys | Infra | 2026-07-25 | High |
| IMPROVE-3 | Annotate dashboards with deploy markers automatically | Platform | 2026-07-31 | Medium |
