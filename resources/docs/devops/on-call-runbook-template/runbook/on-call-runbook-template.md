# On-Call Runbook: `<Service / Team>`

## 1. Alert Index

| Alert Name | Severity | Page? | Runbook Section | Last Verified |
|------------|----------|-------|-----------------|---------------|
| High Error Rate | SEV 2 | Yes | 2.1 | `YYYY-MM-DD` |
| Latency P99 > 2s | SEV 2 | Yes | 2.2 | `YYYY-MM-DD` |
| Disk Usage > 85% | SEV 3 | No | 2.3 | `YYYY-MM-DD` |
| Memory Usage > 90% | SEV 3 | No | 2.4 | `YYYY-MM-DD` |
| SSL Expiry < 7 days | SEV 3 | No | 2.5 | `YYYY-MM-DD` |
| Dependency Unhealthy | SEV 2 | Yes | 2.6 | `YYYY-MM-DD` |
| Job Queue Backlog | SEV 3 | No | 2.7 | `YYYY-MM-DD` |

## 2. Response Procedures

### 2.1. High Error Rate

**Symptoms:**
- Error rate > 1% (or threshold defined in alert)
- Spike in 5xx responses

**Diagnostic Steps:**
1. Check error dashboard for top error types
2. Correlate with recent deployments (last 2 hours)
3. Check downstream dependency health
4. Review application logs for stack traces

**Resolution:**
- If caused by deployment: execute rollback plan
- If caused by dependency failure: see 2.6 Dependency Unhealthy
- If caused by resource exhaustion: see 2.3 or 2.4
- If transient spike: monitor for 10 minutes; auto-recovery common

**Escalation:**
- If error rate > 10% or data-loss errors: page team lead (SEV 1)
- If no root cause within 30 minutes: page team lead

**Anti-patterns — Do NOT:**
- Restart all pods simultaneously (causes cascading failures)
- Scale up without checking if the issue is downstream
- Deploy a fix without testing in staging first
- Close the alert until error rate is below threshold for 15 minutes

### 2.2. Latency P99 > 2s

**Symptoms:**
- P99 latency above threshold
- User complaints about slow responses

**Diagnostic Steps:**
1. Check database query latency
2. Check cache hit rate (Redis / Memcached)
3. Check for N+1 query patterns in logs
4. Check downstream service latency
5. Review CPU and memory utilization

**Resolution:**
- If database bottleneck: kill long-running queries, scale read replicas
- If cache miss storm: pre-warm cache, increase TTL temporarily
- If downstream latency: see 2.6 Dependency Unhealthy

**Escalation:**
- If latency > 10s or affecting > 50% of users: page team lead
- If caused by DDoS: engage security team immediately

### 2.3. Disk Usage > 85%

**Symptoms:**
- Disk usage alert firing
- Risk of write failures

**Diagnostic Steps:**
1. Identify largest directories (`du -sh /* | sort -rh | head`)
2. Check log rotation configuration
3. Check for temporary files or core dumps
4. Check database size and growth rate

**Resolution:**
- Clean old logs (ensure retention policy allows)
- Truncate oversized tables / partitions
- Expand disk if cloud-hosted (AWS EBS, GCP PD)
- Enable log rotation if disabled

**Escalation:**
- If > 95% and writes failing: page team lead
- If expansion fails: page infrastructure team

### 2.4. Memory Usage > 90%

**Symptoms:**
- Memory usage alert firing
- Risk of OOM kills

**Diagnostic Steps:**
1. Identify memory-hungry processes (`ps aux --sort=-%mem | head`)
2. Check for memory leaks (trend over 7 days)
3. Check cache size and eviction rate
4. Check for unbounded queue growth

**Resolution:**
- Restart service if leak suspected (temporary fix)
- Scale to larger instance if sustained growth
- Reduce cache size or TTL
- Fix code leak in next release

**Escalation:**
- If OOM kills causing restarts: page team lead
- If leak root cause unclear: page team lead

### 2.5. SSL Expiry < 7 Days

**Symptoms:**
- Certificate expiration warning

**Diagnostic Steps:**
1. Confirm certificate details and exact expiry date
2. Verify auto-renewal is configured
3. Check if cert is deployed on all endpoints

**Resolution:**
- If auto-renewal failed: manually renew (see cert runbook)
- If manual cert: create renewal ticket for SRE team
- Deploy renewed cert to all load balancers / CDNs

**Escalation:**
- If expiry < 24 hours: page SRE team lead

### 2.6. Dependency Unhealthy

**Symptoms:**
- Downstream service health check failing
- Timeout errors to specific endpoint

**Diagnostic Steps:**
1. Check dependency status page
2. Check dependency metrics dashboard
3. Verify network connectivity (ping, traceroute)
4. Check for DNS resolution issues
5. Verify authentication tokens / API keys not expired

**Resolution:**
- If dependency outage: enable circuit breaker, serve degraded mode
- If network issue: engage network / cloud provider
- If auth issue: rotate credentials
- If capacity issue: request dependency team scale

**Escalation:**
- If dependency is critical and no degraded mode: page team lead + dependency team

### 2.7. Job Queue Backlog

**Symptoms:**
- Queue depth growing
- Processing lag increasing

**Diagnostic Steps:**
1. Check worker process count and health
2. Check worker CPU / memory utilization
3. Check for dead-letter queue growth
4. Review job failure rate

**Resolution:**
- Scale workers horizontally if CPU < 70%
- Restart stuck workers
- Retry failed jobs from dead-letter queue
- If database bottleneck: scale read replicas

**Escalation:**
- If backlog > 1 hour and growing: page team lead
