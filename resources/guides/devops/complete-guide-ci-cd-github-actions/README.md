# CI/CD with GitHub Actions — Companion Workflows

Ready-to-use workflow files from the guide
[Complete Guide to CI/CD with GitHub Actions](https://stackpractices.com/guides/complete-guide-ci-cd-github-actions/).

## Files

- `.github/workflows/ci.yml` — full pipeline: lint, test matrix (Node 18/20/22), build artifact, staging deploy, gated production deploy, concurrency group and least-privilege `permissions`.
- `.github/workflows/test-suite.yml` — reusable test workflow (`workflow_call`) with an optional `node-version` input and `API_KEY` secret.
- `deploy.sh` — placeholder deploy script invoked by the deploy jobs; replace the body with your platform (SSH, `kubectl`, a cloud CLI or a GitOps commit).
- `package.json` — minimal Node project so the workflow's `npm ci`/`lint`/`test`/`build` steps resolve.

## Usage

1. Copy `.github/workflows/` into your repository.
2. Create the `staging` and `production` environments in Settings → Environments, and add required reviewers to `production`.
3. Replace `deploy.sh` with your real deployment and update the environment URLs.
4. Adapt the `paths` filter and the `node-version` matrix to your project.

The deploy jobs only run on `main`; pull requests get lint and the test matrix.
