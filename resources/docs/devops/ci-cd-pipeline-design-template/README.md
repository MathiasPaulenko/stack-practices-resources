# CI/CD Pipeline Design Template Resources

Companion resources for [CI/CD Pipeline Design Template](https://stackpractices.com/docs/ci-cd-pipeline-design-template/).

## Files

| File | Description |
|------|-------------|
| `pipeline/ci-cd-pipeline-design-template.md` | Fill-in design document: pipeline overview, stage and gate tables, environment matrix, deployment strategies, and rollback procedures |
| `ci/github-actions-pipeline.yml` | Complete GitHub Actions workflow implementing the design — build, test + coverage gate, lint, security scan, staging deploy, integration tests, manual approval, blue-green production deploy |
| `ci/gitlab-ci.yml` | Same pipeline expressed in GitLab CI: `stages` ordering, `when: manual` approval gate, `environment` audit trail |
| `scripts/rollback.sh` | Rollback procedures from the template as a runnable script: blue-green switchback, rolling undo, revision rollback, post-rollback verification |

## Usage

1. Copy `pipeline/ci-cd-pipeline-design-template.md` into your repo docs and fill in project, owners, thresholds, and durations.
2. Copy `ci/github-actions-pipeline.yml` to `.github/workflows/` (or `ci/gitlab-ci.yml` to `.gitlab-ci.yml`) and adjust registry, image name, namespaces, and smoke test commands.
3. Keep `scripts/rollback.sh` executable next to your deploy tooling — run `./rollback.sh verify` after any rollback to confirm version, pods, traffic, and logs.
