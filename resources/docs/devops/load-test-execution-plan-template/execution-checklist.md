# Load Test Day Checklist

Print or copy this list into the execution-plan document. Check each item in order during the test window; if a step cannot be verified, do not skip it silently — pause and resolve it first.

## T-1 day

- [ ] Test ID assigned and document shared with all stakeholders
- [ ] Environment window booked and confirmed with SRE
- [ ] Thresholds reviewed and agreed (baseline / target / abort values)
- [ ] Load generator capacity verified (CPU, network, `ulimit -n`, port range)
- [ ] Dashboards open and recording for the full window
- [ ] Rollback or abort plan written and acknowledged

## T-30 min

- [ ] Application versions verified — the build under test is the one you intend
- [ ] Monitoring and alerting confirmed working (test one alert)
- [ ] Auto-scaling policy reviewed; disabled or documented if it must not interfere
- [ ] Load generator health check passed

## T-20 min

- [ ] Environment reset to known state (data seeded, caches cold or warm by design)
- [ ] No other test or deploy scheduled in the same window

## T-10 min

- [ ] Baseline run at low load completed and looks normal
- [ ] Results table open — record numbers during the test, not afterward

## During the test

- [ ] Scenarios executed in the planned order
- [ ] Abort conditions watched on every dashboard check
- [ ] Anomalies noted with timestamps as they happen

## After the test

- [ ] Results and logs exported before the environment is restored
- [ ] Every failed threshold has a finding with owner and due date
- [ ] Environment restored and stakeholders notified of completion
- [ ] Findings filed in the load test report and re-test scheduled
