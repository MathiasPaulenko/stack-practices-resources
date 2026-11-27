# Serverless Throttling Pattern

Runnable companion to the pattern
[Serverless Throttling Pattern](https://stackpractices.com/patterns/serverless-throttling-pattern/).

Three complementary ways to protect downstream services from Lambda burst
traffic: an SQS consumer with a concurrency cap, a DynamoDB token bucket,
and the CDK stack that wires queue + consumer + DLQ together.

## Files

| File | Purpose |
|---|---|
| `sqs_consumer.py` | Lambda consumer with partial batch failure reporting (`batchItemFailures`) and a downstream capacity probe |
| `token_bucket.ts` | DynamoDB-backed token bucket enforcing a precise per-key request rate |
| `throttled_consumer_stack.py` | CDK (Python) stack: queue with long polling + DLQ, consumer capped at 10 concurrent executions |

## Notes

- `sqs_consumer.py` references an `api_client` stub — wire it to your real
  client (`requests`, `httpx`) before deploying.
- Reserved concurrency is sized from the downstream limit, not traffic:
  pool size minus headroom for other callers.
- The token bucket fails closed on DynamoDB errors by default. Wrap
  `allowRequest` and fail open for non-critical endpoints.
