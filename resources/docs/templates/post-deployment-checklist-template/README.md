# Post-Deployment Verification Checklist Template

A copy-paste checklist for verifying that a deployment actually succeeded — health checks, smoke tests, metrics validation, security and log review, rollback readiness, and sign-off.

Source article: [Post-Deployment Verification Checklist Template](https://stackpractices.com/docs/post-deployment-checklist-template/)

## Files

- `post-deployment-checklist-template.md` — blank template ready to fill in per deploy
- `post-deployment-checklist-example.md` — the same checklist filled out for a `payments-api` release

## How to use

1. Copy `post-deployment-checklist-template.md` into your repo (e.g. `docs/deploy-checklist.md`) or your deployment runbook.
2. Fill in the Deployment Info row and run each section in order: health checks first, smoke tests at ~5 minutes, metrics and log review at ~15 minutes.
3. Keep the completed checklist with the deploy record — the sign-off only matters if it's archived.
4. Scale the scope to the risk level: low-risk deploys can run health checks plus a spot smoke test; high-risk deploys get the full checklist, extended monitoring, and a third sign-off.

## Timing guide

| Check | When | Duration |
|-------|------|----------|
| Health checks | Immediately after deploy | ~2 min |
| Smoke tests | ~5 min post-deploy | ~10 min |
| Metrics + security/log review | ~15 min post-deploy | ~10 min |
| Full validation | 1 h post-deploy | Ongoing |
