# Serverless Cold Start Runbook — Companion Resources

Runnable tooling matching the [Serverless Cold Start Runbook](https://stackpractices.com/docs/serverless-cold-start-runbook/) template.

## Contents

| File | Purpose |
|------|---------|
| `warmer.py` | Lambda warmer — invoke functions async to keep containers warm (schedule via EventBridge `rate(5 minutes)`) |
| `cold-start-rate.sh` | Cold start rate over the last hour from CloudWatch logs |
| `cold-start-detection.py` | Module-level `_is_warm` flag pattern for detecting cold starts in Python handlers |

## Usage

```bash
# measure cold start rate
./cold-start-rate.sh /aws/lambda/my-function

# deploy the warmer (serverless.yml snippet in the runbook)
serverless deploy --stage prod
```

Warmers keep costs down vs provisioned concurrency but don't cover concurrency spikes — each concurrent execution path needs its own warm container.
