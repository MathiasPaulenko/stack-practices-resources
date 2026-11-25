# Scheduled Jobs with Serverless Functions — Companion Resources

Runnable files for the [Run Scheduled Jobs with Serverless Functions](https://stackpractices.com/recipes/scheduled-jobs/) recipe on StackPractices.

## Files

| File | What it is |
|------|------------|
| `daily_report_lambda.py` | Python Lambda handler that generates a daily report for the previous day and uploads it to S3. Replace `generate_sales_report` with your real aggregation. |
| `eventbridge_rule.tf` | Terraform for the schedule: EventBridge rule with `cron(0 2 * * ? *)`, the Lambda target, and the `aws_lambda_permission` that lets EventBridge invoke the function. |
| `cloud_scheduler_job.yaml` | Google Cloud Scheduler job definition calling an HTTP Cloud Function with OIDC authentication, at `0 2 * * *` UTC. |
| `timer_trigger_function.py` | Azure Functions Timer Trigger (Python v2 model) running daily at 2:00 AM via the NCRONTAB expression `0 0 2 * * *`. |

## Usage

- **AWS**: zip `daily_report_lambda.py`, deploy it as `report_generator`, then `terraform apply` in a folder containing `eventbridge_rule.tf`. The rule fires daily at 2 AM UTC.
- **GCP**: `gcloud scheduler jobs create http daily-cleanup --schedule="0 2 * * *" --uri=<function-url> --oidc-service-account-email=<sa>` or import the YAML definition.
- **Azure**: drop `timer_trigger_function.py` into a Function App project (Python v2 programming model) and deploy.

All schedules run in UTC by default. Design the handler to be idempotent — the platform may retry and run it twice.
