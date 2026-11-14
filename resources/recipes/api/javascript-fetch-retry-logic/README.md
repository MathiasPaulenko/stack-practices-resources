# JavaScript Fetch Retry Logic — Companion Resources

Companion code for the [JavaScript Fetch Retry Logic with Exponential Backoff](https://stackpractices.com/recipes/javascript-fetch-retry-logic/) recipe on StackPractices.

## Contents

| File | Description |
| --- | --- |
| `fetch_with_retry.js` | Function-style retry: exponential backoff, full jitter, `AbortSignal.timeout`/`any`, `Retry-After` |
| `fetch_retry_breaker.js` | `FetchWithRetry` class + `CircuitBreaker` that counts availability failures only |
| `post_with_retry.js` | Safe POST retries with a shared `Idempotency-Key` |
| `fetch_retry.test.js` | Runnable tests (`node:test` + a `node:http` mock server, zero dependencies) |
| `package.json` | ESM config + `npm test` script |

## Requirements

- Node.js 18+ (ships `fetch`, `AbortSignal.timeout`, `AbortSignal.any`). Node 20+ recommended.

## Running the tests

```bash
npm test
# or directly:
node --test
```

The test suite spins up a real `node:http` server that returns 503/404/429 on demand, so it exercises the retry path over real HTTP — including `Retry-After` handling and breaker accounting. `baseDelay: 1` keeps everything instant.

## Usage

```javascript
import { fetchWithRetry } from "./fetch_with_retry.js";
import { FetchWithRetry } from "./fetch_retry_breaker.js";
import { postWithRetry } from "./post_with_retry.js";

const res = await fetchWithRetry("https://api.example.com/data");

const client = new FetchWithRetry({ retries: 4, breakerThreshold: 5 });
const res2 = await client.request("https://api.example.com/users");

const res3 = await postWithRetry("https://api.example.com/orders", { item: 42 });
```

## Notes

- Retries only availability failures: 5xx, 429, network errors, timeouts. 4xx responses return as-is.
- In Node, `fetch` runs on undici — for service-wide policy look at `undici`'s `RetryHandler` instead of wrapping every call.
- `Idempotency-Key` only helps if the server deduplicates on it; check your API's docs before retrying POSTs.
