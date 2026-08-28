# asyncio.Semaphore: Limit Concurrent API Calls in Python

Companion code for the [StackPractices recipe](https://stackpractices.com/recipes/python-asyncio-semaphore-rate-limiting/).

## Requirements

- Python 3.11+
- No external dependencies for patterns 1, 3, 4, 5, 6, 7 (stdlib only)
- Pattern 2 is simulated (no real HTTP calls)

## Running

```bash
python semaphore_examples.py 1   # Basic Semaphore
python semaphore_examples.py 2   # Rate Limiting API Calls
python semaphore_examples.py 3   # Token Bucket Rate Limiter
python semaphore_examples.py 4   # Per-Host Rate Limiting
python semaphore_examples.py 5   # Database Connection Pool
python semaphore_examples.py 6   # Dynamic Concurrency Adjustment
python semaphore_examples.py 7   # Combining Semaphore with Timeout
```

## Patterns

1. **Basic Semaphore** — 10 workers with max 3 concurrent
2. **Rate Limiting API Calls** — 20 URLs with max 5 concurrent (simulated)
3. **Token Bucket Rate Limiter** — 10 requests at 5/sec with burst capacity 10
4. **Per-Host Rate Limiting** — separate semaphore per hostname, max 2 per host
5. **Database Connection Pool** — 30 queries with max 10 concurrent (simulated)
6. **Dynamic Concurrency Adjustment** — adaptive semaphore that scales up on success
7. **Combining Semaphore with Timeout** — 10 tasks with 0.1s timeout, some intentionally slow
