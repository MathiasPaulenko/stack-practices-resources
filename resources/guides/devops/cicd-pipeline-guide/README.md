# CI/CD Pipeline Guide Resources

Companion resources for [CI/CD Pipeline Guide: From Commit to Production](https://stackpractices.com/guides/cicd-pipeline-guide/).

## Files

| File | Description |
|------|-------------|
| `ci/cicd-pipeline.yml` | Production-ready GitHub Actions pipeline: parallel test/security gates, staging deploy, integration tests, approval-gated production deploy |
| `scripts/rollback.sh` | Kubernetes rollback procedures from the guide as a runnable script: undo, revision rollback, post-rollback verification |

## Usage

1. Copy `ci/cicd-pipeline.yml` to `.github/workflows/` and adjust scripts, environments, and test commands.
2. Keep `scripts/rollback.sh` next to your deploy tooling; run `./rollback.sh verify` after any rollback.
