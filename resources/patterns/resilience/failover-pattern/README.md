# Failover Pattern — Companion Code

Runnable implementations from the
[Failover Pattern](https://stackpractices.com/patterns/failover-pattern/)
on StackPractices — the pattern that moves traffic from a failed primary
system to a healthy standby.

## Files

| File | Description |
|------|-------------|
| `failover/health_monitored.py` | `FailoverManager`: active-passive failover driven by periodic health checks, with separate failure/recovery thresholds to prevent flapping |
| `failover/database.py` | `DatabaseFailover`: PostgreSQL connection manager that probes the active host and walks an ordered standby list |
| `failover/dns.py` | `DNSFailover`: DNS-record failover for multi-region setups (slower, but survives regional outages) |
| `failover/active_active.py` | `ActiveActiveManager`: both nodes serve traffic; a failure just shrinks the healthy pool |
| `failover/cascading.py` | `CascadingFailover`: tries primary → standby → tertiary in order |
| `failover/client.js` | `FailoverClient`: browser/Node client-side failover with periodic health checks |
| `failover/nginx.conf` | Nginx upstream with a `backup` server — passive failover in a few directives |
| `failover/k8s-failover.yaml` | Kubernetes `Service` + `PodDisruptionBudget` sketch for multi-cluster failover behind a global LB |

## Requirements

- Python 3.10+ with `requests`, `psycopg2` (database example), `dnspython` (DNS example)
- Node 18+ for `client.js` (`fetch` and `AbortSignal.timeout` built in)
- A running Nginx or Kubernetes cluster only for the config files

## Usage

```python
from failover.health_monitored import FailoverManager

fo = FailoverManager(
    primary_url="https://api-primary.example.com",
    standby_url="https://api-standby.example.com",
    check_interval=5,       # seconds between health probes
    failure_threshold=3,    # consecutive failures before switching
    recovery_threshold=3,   # consecutive successes before failing back
)
fo.start()

resp = fo.request("GET", "/api/products")   # always hits the active node
```

## Notes

- Thresholds are the whole game: one failed probe is noise, several in a row is
  a signal. The asymmetry between failing over and failing back is deliberate.
- The DNS example stubs `_update_dns` — wire it to your provider's API
  (Route 53, Cloudflare, etc.).
- In production, prefer managed failover (RDS, Cloud SQL, `repmgr`, HAProxy,
  cloud load balancers) over hand-rolled loops; these files exist to teach the
  semantics.
