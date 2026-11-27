# Serverless Function Deployment Checklist — Companion Resources

Runnable assets matching the [Serverless Function Deployment Checklist](https://stackpractices.com/docs/serverless-function-deployment-checklist/).

## Contents

| File | Purpose |
|------|---------|
| `deploy.sh` | Deployment pipeline: unit/integration tests, package, deploy, smoke tests, verify |
| `serverless.yml` | Reference Serverless Framework config: sizing, least-privilege IAM, per-stage env vars, API Gateway + SQS events, CloudWatch alarms, canary rollout via CodeDeploy |

## Usage

```bash
# deploy to staging (default) or prod
./deploy.sh staging
./deploy.sh prod

# or deploy with Serverless Framework directly
npx serverless deploy --stage prod
```

The `serverless.yml` is a reference, not a drop-in: replace ARNs, bucket names, SSM parameter paths and the `AlertTopic`/`OrderQueue` resources with your own before deploying. The canary rollout only protects you if the referenced alarms exist — they are defined under `resources:` in the same file.
