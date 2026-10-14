# Retry Logic with Exponential Backoff

Runnable companion code for the recipe [Retry Logic with Exponential Backoff](https://stackpractices.com/recipes/retry-logic-exponential-backoff/) on StackPractices.

## Contents

| File | Language | What it shows |
| --- | --- | --- |
| `retry.py` | Python | `@retry` decorator: exponential backoff, full jitter, exception filtering, `on_retry` hook, injectable `sleep` |
| `test_retry.py` | Python | pytest suite — verifies the exact delay sequence, jitter bounds, exception filtering, and the retry callback using a fake sleep |
| `retry.js` | JavaScript | `retry()` helper with HTTP status filtering, idempotency-key example, injectable `sleep` |
| `Retry.java` | Java | `Retry.execute()` with injectable `Sleeper` and retryable-exception filtering |
| `retry.go` | Go | `withRetry()` with context deadline and jitter via `math/rand` |

## Run

```bash
python retry.py              # demo: flaky function succeeds on attempt 3
python -m pytest test_retry.py -v

node retry.js                # demo without network access

javac Retry.java && java Retry

go run retry.go
```

The demos and tests never hit the network and never actually sleep — the `sleep`/delay function is injectable so the backoff sequence is asserted directly.
