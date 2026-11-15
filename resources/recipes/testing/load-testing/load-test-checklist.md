# Load Test Pre-Flight Checklist

Run through this before every load test that matters.

## Target

- [ ] Environment is production-like (same instance sizes, same data volume order of magnitude)
- [ ] Server-side monitoring is on: CPU, memory, slow query log, connection pool stats
- [ ] No deploys, backups, or batch jobs scheduled inside the test window
- [ ] Write-heavy endpoints use synthetic data with a cleanup plan (unique prefix, teardown script)
- [ ] Alert channels know a test is running (no pages at 3am for expected load)

## Generator

- [ ] Generator CPU stays below ~80% during the run (add machines or use distributed mode)
- [ ] File descriptor limit raised: `ulimit -n` ≥ 65535 on Linux
- [ ] Ephemeral port range checked: `netsh int ipv4 show dynamicport tcp` / `sysctl net.ipv4.ip_local_port_range`
- [ ] Generator runs in the same region as the target (unless measuring WAN latency is the goal)
- [ ] Arrival-rate executor used when offered load matters (closed VU model hides queueing)

## Script

- [ ] Warm-up stage (5 min) precedes measurement
- [ ] Thresholds defined before the run: p95 latency, error rate, plus `abortOnFail` for risky targets
- [ ] Test duration ≥ 10 min for smoke, ≥ 30 min for release gates, hours for soak tests
- [ ] Responses validated on body content, not just status codes
- [ ] Auth tokens fetched once in `setup()`, not per iteration
- [ ] Test data parameterized (CSV/SharedArray) — no hard-coded payloads that become cache tests

## After the run

- [ ] Results stored as baseline (JSON export or Prometheus remote-write)
- [ ] Percentiles compared against previous run, not just the SLO
- [ ] Test data cleaned up
- [ ] Findings written down: bottleneck layer, fix applied, re-test date
