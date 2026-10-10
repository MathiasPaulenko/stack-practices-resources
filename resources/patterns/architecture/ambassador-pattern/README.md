# Ambassador Pattern — Infrastructure Proxy Examples

Runnable examples for the [Ambassador pattern](https://stackpractices.com/patterns/ambassador-pattern/) resource on StackPractices.

An ambassador is a proxy that sits between clients and external services and takes over the cross-cutting concerns: connection pooling, retries, circuit breaking, monitoring, and TLS termination. Clients talk to the ambassador as if it were the real service.

## Contents

| File | What it is |
|------|------------|
| `envoy-ambassador.yaml` | Envoy listener + cluster: TLS upstream, retry policy, circuit breaker thresholds |
| `ambassador_proxy.py` | Python ambassador: retries with exponential backoff, circuit breaker, per-endpoint stats |
| `client_example.py` | Client calling the ambassador instead of the real API |
| `AmbassadorClient.java` | Java 11+ ambassador (`java.net.http`), same policy chain |
| `nginx-stream-ambassador.conf` | Nginx `stream` block proxying raw TCP (PostgreSQL) with failover |
| `requirements.txt` | Python dependency (`requests`) |

## Quick start

Python ambassador:

```bash
pip install -r requirements.txt
python client_example.py
```

Point `AmbassadorProxy("https://api.external.com")` at any endpoint — e.g. `python -m http.server 8080` locally for a smoke test.

Envoy ambassador:

```bash
envoy -c envoy-ambassador.yaml
curl http://localhost:18080/users/42   # forwarded to api.external.com:443
```

Nginx stream ambassador: copy the block into your `nginx.conf` at top level (outside `http {}`), then connect Postgres clients to the Nginx host on port 5432.
