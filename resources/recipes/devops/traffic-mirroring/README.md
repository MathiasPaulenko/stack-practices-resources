# Traffic Mirroring Companion

Runnable configs for traffic mirroring with Nginx, Istio, Envoy, and GoReplay.

## Files

| File | Description |
|------|-------------|
| `nginx.conf` | Nginx mirror module config with health check and static asset filtering |
| `istio-virtualservice.yaml` | Istio VirtualService + DestinationRule for 10% mirroring |
| `envoy.yaml` | Envoy static config with request mirror policy at 10% |
| `goreplay-commands.sh` | GoReplay CLI commands for capture, replay, and filtering |
| `response_comparison.js` | Express middleware that mirrors traffic and diffs responses |
| `test_mirror.py` | pytest tests for connectivity, idempotency, schema, auth stripping, latency |
| `docker-compose.yml` | Docker Compose with production + staging Nginx + GoReplay |

## Quick Start

```bash
# Start production and staging with Nginx mirror
docker-compose up -d

# Run tests
pip install -r requirements.txt
pytest test_mirror.py -v
```

## Related Resource

[Traffic Mirroring for Production Testing](https://stackpractices.com/recipes/traffic-mirroring/)
