# Complete Guide to AWS Lambda in Production — Companion Code

Runnable building blocks for the guide
[Complete Guide to AWS Lambda in Production](https://stackpractices.com/guides/complete-guide-aws-lambda-production/)
on StackPractices.

## Files

| File | What it implements |
| --- | --- |
| `cold_start_tracker.py` | Init vs handler timing instrumentation |
| `structured_logger.py` | JSON logging with `request_id` on every line |
| `rds_proxy_client.py` | RDS Proxy connection with `finally` cleanup |
| `secrets_cache.py` | Secrets Manager + `lru_cache` module-scope caching |
| `idempotent_handler.py` | Event-hash idempotency key + Redis dedup |
| `sqs_batch_handler.py` | SQS `batchItemFailures` partial retry |
| `template.yaml` | SAM template: alias + canary + rollback alarm |
| `deploy-canary.sh` | Alias traffic-shift script |
| `test_lambda_patterns.py` | pytest smoke tests (fakeredis, mocks) |

## Setup

```bash
pip install -r requirements.txt
pip install fakeredis pytest
pytest test_lambda_patterns.py -v
```

App-provided dependencies (`redis_client`, `process_event`, `process_message`,
`secret`) are injected so the modules stay testable without AWS credentials.
