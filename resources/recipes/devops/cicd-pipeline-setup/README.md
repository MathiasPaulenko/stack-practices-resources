# CI/CD Pipeline Setup Resources

Companion resources for [CI/CD Pipeline Setup](https://stackpractices.com/recipes/cicd-pipeline-setup/).

## Files

| File | Description |
|------|-------------|
| `ci/deploy.yml` | GitHub Actions pipeline: test, security scan, staging and gated production deploy |
| `ci/gitlab-ci.yml` | Same pipeline in GitLab CI: stages, coverage regex, protected production environment |
| `ci/blue-green.yml` | Blue-green deploy job: detects active color, deploys to inactive, switches traffic, rolls back on failed smoke test |
| `ci/rollout-canary.yaml` | Argo Rollouts canary: 10% → 25% → 50% → 100% with pauses |

## Usage

Copy into `.github/workflows/` (or `.gitlab-ci.yml`), adjust image names, environments, and deploy commands.
