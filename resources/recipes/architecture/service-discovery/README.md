# Service Discovery — Companion Code

Runnable examples for the [Service Discovery](https://stackpractices.com/recipes/service-discovery/) recipe on StackPractices.

## Files

| File | What it shows |
| --- | --- |
| `consul_register.go` | Consul registration with an HTTP health check, `DeregisterCriticalServiceAfter`, and graceful deregistration on SIGTERM — a crashed process cleans itself up. |
| `consul_discovery.py` | Client-side discovery with a 30-second local cache plus a no-expiry "last known good" fallback, so a registry outage doesn't take your clients down. Requires `python-consul` and `requests`. |
| `health_check.go` | Split liveness/readiness handlers: liveness restarts the process, readiness drops it from the pool during warm-up or dependency failures. |
| `istio-traffic.yaml` | VirtualService (90/10 canary + retries) and DestinationRule (LEAST_REQUEST + outlier detection) — traffic policy on top of Kubernetes discovery. |
| `pooled_client.py` | Per-instance connection pooling: one `requests.Session` per discovered URL instead of a fresh TCP handshake per request. |

## Quick start

```bash
# Requires a Consul agent on localhost:8500
go run consul_register.go

pip install python-consul requests
python consul_discovery.py

go run health_check.go
curl localhost:8080/ready

kubectl apply -f istio-traffic.yaml
```

## What to adapt for production

- The 30-second client cache plus a 10-second health check means a dead
  instance keeps receiving traffic for up to ~40 seconds — that's why
  retries on connection errors aren't optional.
- `DeregisterCriticalServiceAfter` is your safety net for processes that
  die without deregistering; don't leave it unset.
- On Kubernetes, you usually don't need a separate registry at all —
  CoreDNS + Endpoints is the discovery layer, Istio just adds policy.
