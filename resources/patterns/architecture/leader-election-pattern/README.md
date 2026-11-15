# Leader Election Pattern — Companion Code

Runnable implementations for the [Leader Election Pattern](https://stackpractices.com/patterns/leader-election-pattern/) resource on StackPractices.

## Files

| File | What it shows |
| --- | --- |
| `leader_election.py` | Self-contained demo: atomic CAS store + fencing tokens, simulated crash and failover. Runs with plain Python 3 — no services needed. |
| `leader-election-etcd.py` | Election over etcd's `client.transaction` with a TTL lease (python-etcd3). Needs etcd on `localhost:2379`. |
| `leader-election-redis.py` | `SET key token NX PX` acquire + Lua compare-and-delete / compare-and-renew. Needs Redis on `localhost:6379`. |
| `leader-election-k8s.go` | client-go update loop against the Kubernetes `Lease` API. |
| `lease.yaml` | Raw `coordination.k8s.io/v1` Lease manifest for `kubectl apply -f`. |

## Quick start

```bash
python leader_election.py
```

Expected output: `node-1` wins the lease, renews it twice, crashes, and a
follower takes over with a higher fencing token.

For the etcd and Redis variants, start the service first:

```bash
docker run -d -p 2379:2379 gcr.io/etcd-development/etcd:v3.5.11
pip install etcd3 && python leader-election-etcd.py

docker run -d -p 6379:6379 redis:7
pip install redis && python leader-election-redis.py
```

## Why fencing tokens matter

Every implementation here returns or carries a monotonic token
(`fence` in `leader_election.py`, `mod_revision` in etcd, the token value in
Redis). Downstream services must reject writes carrying a lower token —
that's the only reliable way to stop a paused or partitioned ex-leader
from still writing as if it were in charge.
