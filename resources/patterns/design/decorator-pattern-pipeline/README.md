# Decorator Pattern for HTTP Request Pipelines — Companion Code

Companion code for [Decorator Pattern for HTTP Request Pipelines](https://stackpractices.com/patterns/decorator-pattern-pipeline/) on StackPractices.

## What's inside

| File | Role |
|------|------|
| `src/HttpClient.ts` | Shared interface every layer implements |
| `src/FetchClient.ts` | Innermost client — thin wrapper over `fetch` |
| `src/BaseClientDecorator.ts` | Abstract base holding the inner `HttpClient` reference |
| `src/LoggingDecorator.ts` | Logs method, URL, status, and wall time |
| `src/RetryDecorator.ts` | Selective retry: `response.ok` check, 502/503/504 + network errors only, exponential backoff with jitter |
| `src/AuthDecorator.ts` | Injects `Authorization: Bearer` header on every request, including retries |
| `src/CircuitBreakerDecorator.ts` | Closed → open → half-open state machine; probe request after `resetTimeout` |
| `src/httpClientFactory.ts` | `createHttpClient(config)` builds the full stack |
| `demo.ts` | Runs one GET against JSONPlaceholder through the whole stack |

## Run it

Requires Node 20+ (native `fetch`) and `tsx` or `ts-node`:

```bash
npx tsx demo.ts
```

Expected output:

```text
GET https://jsonplaceholder.typicode.com/todos/1 → 200 (XXXms)
status: 200
body: { userId: 1, id: 1, title: 'delectus aut autem', completed: false }
```

## Key details

- `fetch` resolves on HTTP errors — `RetryDecorator` checks `response.ok` and retries only 502/503/504 plus network failures.
- Decorator order in the factory: `Auth → Retry → Logging → CircuitBreaker → Fetch`. Auth outermost so retries carry the token; circuit breaker innermost so it sees raw network failures.
- Each decorator clones `options` before mutating headers, so retries don't accumulate duplicated state.
