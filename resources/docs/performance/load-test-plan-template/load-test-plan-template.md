# Load Test Plan — {Service Name}

> Fillable plan document. Fill each section before running the test.
> Source: <https://stackpractices.com/docs/load-test-plan-template/>

## 1. Test Objectives

| Objective | Question answered | Selected |
|-----------|-------------------|----------|
| Baseline performance | What is current throughput and latency? | [ ] |
| Capacity validation | Can we handle expected peak traffic? | [ ] |
| Bottleneck identification | Where does the system break first? | [ ] |
| Scalability validation | Does horizontal scaling work as expected? | [ ] |
| Regression detection | Did the latest deploy degrade performance? | [ ] |
| Endurance / soak | Does memory leak over 24h of load? | [ ] |
| Spike readiness | Can we survive a 10x traffic spike? | [ ] |

Primary goal for this test: {describe in one sentence}

## 2. Scope

In scope: {endpoints, flows, environments}
Out of scope: {third-party APIs, browser rendering, security testing}

## 3. User Journeys

| Journey name | Steps | % of traffic | Requests/user |
|--------------|-------|--------------|---------------|
| {e.g. Browse} | GET / → GET /api/products | 40% | 2 |
| | | | |

Test data: {sources and volumes — product IDs, accounts, queries, tokens}

## 4. Load Profile

| Test phase | Duration | Users | Ramp rate | Purpose |
|------------|----------|-------|-----------|---------|
| Warmup | 2 min | 10 | 5/sec | JIT compilation, caches |
| Baseline | 10 min | 50 | 5/sec | Normal load baseline |
| Ramp-up | 5 min | 200 | 30/sec | Peak traffic simulation |
| Peak hold | 15 min | 200 | - | Sustained peak performance |
| Ramp-down | 2 min | 0 | -/sec | Graceful shutdown |

## 5. Success Criteria

| Metric | Target | Hard limit | Failure action |
|--------|--------|------------|----------------|
| P50 response time | < 100ms | < 200ms | Investigate |
| P95 response time | < 300ms | < 500ms | Investigate |
| P99 response time | < 500ms | < 1000ms | Investigate |
| Error rate | < 0.1% | < 1% | Stop test |
| Throughput (req/sec) | > 500 | > 300 | Investigate |
| CPU usage | < 70% | < 90% | Scale up |
| Memory usage | < 75% | < 90% | Investigate leaks |
| DB connection pool | < 60% | < 80% | Increase pool |

## 6. Tool and Environment

- Tool: {k6 / JMeter / Locust / Artillery / Gatling}
- Environment: {staging mirroring production — specs:}
- Load generator host: {separate machine/region:}

## 7. Monitoring

Dashboards/queries wired before the test: {links to Grafana panels, alert channels muted/notified}
Stakeholders notified: {date, channel}

## 8. Report

Fill `report-template.md` during the test. Schedule the re-run after fixes: {date/owner}
