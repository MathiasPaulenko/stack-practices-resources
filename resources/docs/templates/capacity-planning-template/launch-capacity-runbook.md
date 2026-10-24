# Product Launch Capacity Runbook

System: E-commerce platform
Event: New product launch (Q3)
Expected traffic: 3x normal peak for 2 weeks

Step 1 - Collect baseline data:
  $ kubectl top pods -n production --sort-by=cpu
  $ aws cloudwatch get-metric-statistics \
      --namespace AWS/RDS \
      --metric-name DatabaseConnections \
      --start-time 2026-06-01 --end-time 2026-06-30 \
      --period 3600 --statistics Average,Maximum

  Results:
  - API servers: 6 instances, CPU peak 72%, memory peak 68%
  - DB connections: peak 140 of 200 max (70% utilization)
  - RPS peak: 18,000 of 25,000 limit (28% headroom)

Step 2 - Project launch load:
  - Expected peak RPS: 18,000 * 3 = 54,000
  - Expected DB connections: 140 * 3 = 420 (exceeds 200 max)
  - Expected API CPU: 72% * 3 = 216% (exceeds 100% per instance)

Step 3 - Identify bottlenecks:
  1. DB connections: exhausted at 200 (critical)
  2. API CPU: need 3x instances or optimization
  3. Bandwidth: 450 Mbps * 3 = 1,350 Mbps (exceeds 1 Gbps)

Step 4 - Mitigation plan:
  - DB: add 2 read replicas + connection pooling (pgbouncer)
    Config: pool_mode=transaction, max_client_conn=500
  - API: add 12 instances to burst pool (total 18)
    Auto-scaling: min=6, max=20, target CPU=60%
  - Network: upgrade to 2 Gbps + enable CDN for static assets
  - Pre-warm: scale to 18 instances 1 hour before launch

Step 5 - Load testing:
  $ k6 run --vus 500 --duration 10m launch_test.js
  $ locust -f locustfile.py --host https://staging.example.com \
      --users 1000 --spawn-rate 50

  Acceptance criteria:
  - P99 latency < 500ms at 50k RPS
  - Error rate < 0.1%
  - DB connections < 180 with pooling
  - CPU < 70% across all instances

Step 6 - Rollback plan:
  - If error rate > 1%: enable degraded mode (rate limiting)
  - If DB connections > 190: activate circuit breaker on reads
  - If CPU > 85% for 5 min: manually scale to 24 instances
