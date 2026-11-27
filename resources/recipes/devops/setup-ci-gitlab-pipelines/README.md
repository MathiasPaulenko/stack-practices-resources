# Setup CI with GitLab Pipelines — Companion Project

Runnable companion for the [Setup CI with GitLab Pipelines recipe](https://stackpractices.com/recipes/setup-ci-gitlab-pipelines/) on StackPractices.

## Contents

- `.gitlab-ci.yml` — root pipeline configuration using top-level includes.
- `.gitlab/ci/test.yml` — Node test job.
- `.gitlab/ci/build.yml` — build job that publishes `dist/` as an artifact.
- `.gitlab/ci/deploy.yml` — manual staging job that packages `dist/` and uploads it to GitLab's Generic Package Registry with the CI job token.
- `package.json` and `package-lock.json` — reproducible Node setup using `npm ci`.
- `.gitignore` — keeps `node_modules/` and generated `dist/` out of version control while allowing the lockfile needed by `npm ci`.
- `src/index.js`, `test/index.test.js`, `scripts/build.js` — minimal application, test, and build scripts.

## Try it locally

```bash
npm ci
npm test
npm run build
```

The deploy job is manual and runs only on the default branch. It uses predefined GitLab variables (`CI_JOB_TOKEN`, `CI_API_V4_URL`, `CI_PROJECT_ID`, `CI_PIPELINE_IID`, and `CI_COMMIT_SHORT_SHA`), so no external server is required. If your organization disables the package registry, replace the `curl` step with your deployment command.
