# Deployment Checklist: api-billing v2.4.0

| Field | Value |
|-------|-------|
| Service | api-billing |
| Version | 2.4.0 |
| Branch / Commit | main@f31c9d2 |
| Deployer | @mpaulenko |
| Date | 2026-10-16 14:00 UTC |
| Ticket / PR | BILL-882 |

## Pre-Deployment

- [x] CI green on PR #412, approved by two senior engineers
- [x] Migration `20261015_add_refund_reason.sql` tested on a production copy (12 min)
- [x] Rollback image `api-billing:2.3.9` tagged in the registry
- [x] Feature flag `refund_v2` configured, defaulted off
- [x] #deployments channel notified, on-call engineer confirmed

## Deployment

- [x] Migration ran in 11 min — expand only, no drops
- [x] Canary at 10% for 10 min: error rate 0.02%, p95 180ms (baseline 172ms)
- [x] Full rollout completed at 14:35 UTC

## Post-Deployment

- [x] `refund_v2` enabled 5% → 25% → 100% over 2 hours
- [x] No new Sentry issues during the 30-minute watch window
- [x] Old pods scaled to 0 at 15:10 UTC
- [ ] Checklist review scheduled after next incident review
