# GitHub Actions Reusable Workflows — Examples

Companion code for the StackPractices recipe:
https://stackpractices.com/recipes/github-actions-reusable-workflows/

## What's inside

Reusable workflows (callable via `workflow_call`):

| File | Purpose |
|---|---|
| `.github/workflows/reusable-build.yml` | Basic reusable build with typed `node-version` and `run-tests` inputs |
| `.github/workflows/reusable-deploy.yml` | Deploy gated by `environment` input + required/optional secrets |
| `.github/workflows/reusable-test-matrix.yml` | Matrix passed as JSON input and expanded with `fromJSON` |
| `.github/workflows/reusable-ci.yml` | Conditional jobs driven by boolean inputs (`skip-lint`, `deploy`) |
| `.github/workflows/reusable-build-with-output.yml` | Exposes `artifact-url` through `workflow_call.outputs` |
| `.github/workflows/reusable-docker-build.yml` | Docker build/push to GHCR with explicit `permissions` |
| `.github/workflows/reusable-quality.yml` | Nested example: orchestrates the build and test-matrix workflows |

Caller workflows:

| File | Purpose |
|---|---|
| `.github/workflows/ci.yml` | Calls the build and matrix workflows on push/PR |
| `.github/workflows/deploy.yml` | Staging → production chain with `needs` and mapped secrets |
| `.github/workflows/release.yml` | Tag-triggered release that consumes `artifact-url` output |

## How to use

1. Copy the files you need into your repository, keeping the `.github/` directory layout.
2. Create the `STAGING_DEPLOY_TOKEN`, `PROD_DEPLOY_TOKEN` and `REGISTRY_PASSWORD` secrets under **Settings > Secrets and variables > Actions**.
3. Create `staging` and `production` environments under **Settings > Environments** if you want approval gates.
4. `./deploy.sh` is a placeholder — point the deploy steps at your own script or action.
5. To call a workflow from another repo, reference it by path and ref:

```yaml
jobs:
  call-build:
    uses: my-org/shared-workflows/.github/workflows/reusable-build.yml@v1
    with:
      node-version: '20'
```

Private or internal repositories must enable Actions access for other repos in the organization (**Settings > Actions > General > Access**).

## Notes

- Pin callers to a tag or SHA (`@v1`) instead of `@main` so a changed workflow does not break consumers.
- Keep `workflow_call` as the only trigger on reusable workflows — mixing it with `push` or `pull_request` fires them on their own repo's events too.
