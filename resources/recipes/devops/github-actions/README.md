# GitHub Actions — Runnable Workflow Examples

Companion code for the StackPractices recipe:
https://stackpractices.com/recipes/github-actions/

## What's inside

| File | Purpose |
|---|---|
| `.github/workflows/ci.yml` | Node.js CI pipeline on push and PR to `main` |
| `.github/workflows/test-matrix.yml` | Reusable matrix workflow (3 OS × 3 Node versions, `workflow_call`) |
| `.github/workflows/reusable-lint.yml` | Reusable lint workflow with a required `node-version` input |
| `.github/workflows/deploy.yml` | Tag-triggered deploy gated by a `production` environment and a concurrency group |
| `.github/workflows/nightly-audit.yml` | Cron-scheduled `npm audit` at 03:00 UTC plus `workflow_dispatch` |
| `.github/actions/setup-project/action.yml` | Composite action: setup Node + cache + `npm ci` + build |

## How to use

1. Copy the files you need into your repository, keeping the `.github/` directory layout.
2. Create the `DEPLOY_TOKEN` secret under **Settings > Secrets and variables > Actions**.
3. Create a `production` environment under **Settings > Environments** if you want the approval gate in `deploy.yml`.
4. Call a reusable workflow from another repo:

```yaml
jobs:
  call-lint:
    uses: org/shared-workflows/.github/workflows/reusable-lint.yml@main
    with:
      node-version: '20'
```

5. Reference the composite action locally:

```yaml
steps:
  - uses: actions/checkout@v4
  - uses: ./.github/actions/setup-project
    with:
      node-version: '22'
```

For the full explanation — execution model, contexts, `GITHUB_TOKEN`, concurrency, billing multipliers — read the recipe.
