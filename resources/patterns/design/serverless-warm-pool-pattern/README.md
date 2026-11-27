# Serverless Warm Pool Pattern

Runnable companion to the pattern
[Serverless Warm Pool Pattern](https://stackpractices.com/patterns/serverless-warm-pool-pattern/).

A CDK stack that keeps a Lambda API warm: an EventBridge rule invokes a
small warmup function every 5 minutes, which sends N concurrent async
pings to the API function. The API function short-circuits on the
`isWarmup` flag, so each ping keeps one execution environment alive
without triggering business logic.

## Files

| File | Purpose |
|---|---|
| `warm_pool_stack.py` | CDK (Python) stack: API function, warmup function, EventBridge schedule, invoke permission |
| `warmup_handler.py` | Warmup Lambda that fans out N concurrent async pings with `ThreadPoolExecutor` |
| `warmup_handler.ts` | Same warmup handler with AWS SDK v3 and `Promise.all` |
| `api_handler.py` | API handler with `isWarmup` early return (Python) |
| `api_handler.ts` | API handler with `isWarmup` early return (TypeScript) |

## Notes

- `WARM_COUNT` sizes the warm pool — set it to expected *concurrent*
  requests, not traffic volume.
- The ping interval is 5 minutes; Lambda environments typically expire
  after 5-15 minutes idle. Shorter intervals waste invocations.
- The warmup function needs `lambda:InvokeFunction` on the target ARNs —
  the stack grants it via `api_function.grant_invoke`.
- For guaranteed warm capacity on strict SLAs, prefer provisioned
  concurrency or Lambda SnapStart over scheduled pings.
