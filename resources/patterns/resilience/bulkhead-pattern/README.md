# Bulkhead Pattern — Companion Code

Runnable implementations of the bulkhead pattern: isolate threads, connections, and concurrent calls per service or tenant so one saturated dependency can't starve the rest.

Source article: [Bulkhead Pattern: Isolate Resources to Limit Blast Radius](https://stackpractices.com/patterns/bulkhead-pattern/)

## Files

| File | What it shows |
|------|---------------|
| `exceptions.py` | Shared `BulkheadFullError` and `CircuitBreakerOpenError` used by the other modules. |
| `thread_pool.py` | `BulkheadManager` — a dedicated `ThreadPoolExecutor` per service with bounded queues and fail-fast rejection. |
| `semaphore.py` | `SemaphoreBulkhead` — concurrency limiting with a semaphore; usable as a decorator or context manager. |
| `connection_pools.py` | `IsolatedConnectionPools` — separate psycopg2 connection pools for critical vs non-critical paths. Requires `psycopg2-binary`. |
| `per_tenant.py` | `PerTenantBulkhead` — per-tenant semaphore so one noisy tenant can't exhaust shared capacity. |
| `hybrid.py` | `BulkheadWithCircuitBreaker` — concurrency limit plus failure-based circuit breaking in one wrapper. |
| `ServiceBulkheads.java` | resilience4j `Bulkhead` and `ThreadPoolBulkhead` configuration for sync and async calls. |
| `k8s-bulkhead.yaml` | `ResourceQuota` per namespace plus per-pod CPU/memory limits — bulkheads enforced by the platform. |

## Usage

```bash
python thread_pool.py      # prints a submitted task result and pool stats
python semaphore.py        # runs a decorated and a context-managed call
python per_tenant.py       # acquires permits for three tenants, prints stats
python hybrid.py           # one call through the combined bulkhead + breaker
```

`connection_pools.py` needs a reachable PostgreSQL and `pip install psycopg2-binary`. `ServiceBulkheads.java` needs `io.github.resilience4j:resilience4j-bulkhead` on the classpath and real `paymentClient`/`inventoryClient` implementations.

## Notes

- Every bulkhead rejects on saturation (`BulkheadFullError`) instead of blocking — that's the fail-fast half of the pattern.
- `thread_pool.py` tracks `_active` in a `defaultdict` without a lock for readability; use a `threading.Lock` if you submit from multiple threads.
- The K8s quotas isolate *namespaces*; pod-level `resources` isolate individual containers. Use both.
