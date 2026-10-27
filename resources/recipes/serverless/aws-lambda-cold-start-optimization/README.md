# Reduce AWS Lambda Cold Start — Companion Files

Runnable companion for the [Lambda cold start recipe](https://stackpractices.com/recipes/aws-lambda-cold-start-optimization/) on StackPractices.

- `measure_cold_start.py` — module-level flag pattern to detect cold starts inside the handler.
- `lazy_init.py` — deferred imports/data loading for heavy dependencies (pandas example).
- `reuse_connections.py` — module-level boto3 client reuse across warm invocations.
- `powertools_logging.py` — structured logging with AWS Lambda Powertools.
- `minimal_handler.py` — raw routing handler instead of a heavy framework.
- `cloudwatch-insights-query.txt` — Logs Insights query for Init Duration stats.
- `template.yaml` / `snapstart-template.yaml` / `efs-template.yaml` — SAM configs: provisioned concurrency, SnapStart (Java), EFS mount.
- `serverless.yml` — Serverless Framework warm-up plugin config.
- `package-trim.sh` / `arm64-migration.sh` — strip dev files from the package and rebuild layers for Graviton.
