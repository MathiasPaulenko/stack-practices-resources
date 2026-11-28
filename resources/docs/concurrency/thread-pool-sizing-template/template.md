# Thread Pool Configuration — <service-name>

```text
=== Thread Pool Configuration: <service-name> ===
Pool name:            <e.g., image-resize-pool>
Workload type:        [ ] CPU-bound   [ ] I/O-bound   [ ] Mixed
Measured W/C ratio:   <wait ms / compute ms, from profiler>
N_cpu (quota-aware):  <logical cores or cgroup CPU limit>
Arrival rate (peak):  <req/s at p99 load>
Target latency:       <p99 ms, from SLO>

Computed size:
  threads      = <N_cpu or N_cpu * (1 + W/C)>
  core / max   = <corePoolSize> / <maxPoolSize>
  queue        = <from Little's Law: L - active>
  keepAlive    = <seconds>

Rejection policy:     <CallerRunsPolicy / custom>
Rationale:            <why this policy — what should happen on overload>

Runtime config:       <file / env var / annotation where it lives>
Metrics emitted:      <active, queue.depth, rejected, task.duration>
Alerts:               <thresholds wired to pager>
Load-test evidence:   <link to test run proving the numbers>
Review date:          <when to re-measure W/C>
```

## Notes

- `N_cpu` in containers: the runtime may report host cores instead of the cgroup quota. In Java use `-XX:ActiveProcessorCount` or a JVM that reads the quota; check `runtime.NumCPU` in Go and `os.availableParallelism()` in Node.js against the container limit.
- Measure W/C under real load, not in a quiet staging environment — the ratio shifts when a downstream dependency slows down.
- If the computed size exceeds a downstream limit (connection pool, rate limit), the downstream limit wins; size for the scarce resource.
