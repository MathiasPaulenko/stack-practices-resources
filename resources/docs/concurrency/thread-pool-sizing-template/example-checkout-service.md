# Thread Pool Configuration — checkout-service

```text
=== Thread Pool Configuration: checkout-service ===
Pool name:            inventory-api-pool
Workload type:        [ ] CPU-bound   [x] I/O-bound   [ ] Mixed
Measured W/C ratio:   200ms wait / 20ms compute = 10 (async-profiler, prod)
N_cpu (quota-aware):  4 (cgroup limit, container sees 4 not 32 host cores)
Arrival rate (peak):  400 req/s at p99
Target latency:       p99 < 800 ms

Computed size:
  threads      = 4 * (1 + 10) = 44
  core / max   = 44 / 88
  queue        = Little's Law: 400 * 0.22 = 88 in system, 88 - 44 = 44 -> 100
  keepAlive    = 60s

Rejection policy:     CallerRunsPolicy
Rationale:            Checkout must not drop work silently; slowing the HTTP
                      handler is the correct degradation under overload.

Runtime config:       application.yml -> executor.inventory (Spring @Bean)
Metrics emitted:      threadpool.active, threadpool.queue.size,
                      threadpool.pool.size, threadpool.peak (Micrometer)
Alerts:               ThreadPoolQueueBacklog >80% 5m; ThreadPoolRejections >0
Load-test evidence:   loadtest-run-2026-11: queue depth peak 61, 0 rejections,
                      p99 640ms
Review date:          2027-01-15 or when inventory API p50 latency changes
```

## Notes

- Validated under load test: queue peaked at 61/100, zero rejections, p99 640 ms — inside the 800 ms SLO.
- If the inventory API's latency doubles, W/C doubles and `threads = 4 * (1 + 20) = 84` — re-run the worksheet instead of guessing.
