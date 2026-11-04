# GraphQL Federation in Production — Companion Resources

Production-ready configuration files for the guide
[GraphQL Federation in Production](https://stackpractices.com/guides/complete-guide-graphql-federation-production/).

## Contents

| File | Purpose |
| --- | --- |
| `router.yaml` | Apollo Router production config: health checks, timeouts, persisted queries, limits, CSRF, header propagation, OTel export |
| `supergraph.yaml` | Rover supergraph composition config for self-hosted mode |
| `docker-compose.yml` | Managed-federation router container (Uplink polling) |
| `k8s/deployment.yaml` | 3-replica router Deployment with probes on port 8088 |
| `schema-ownership.yaml` | Machine-readable type/field ownership map |
| `src/users-subgraph.js` | Users subgraph with `__resolveReference` (batch it in real code) |
| `ci/check-schema.sh` | CI step: `rover subgraph check` before publish |

## Usage

```bash
# Compose the supergraph locally
rover supergraph compose --config supergraph.yaml > supergraph.graphql

# Run the router against the composed file
./router --supergraph supergraph.graphql --config router.yaml

# Or managed mode (polls Uplink)
docker compose up
```

Health checks live on port `8088` (`/health`, `?live`, `?ready`). Widen
`health_check.listen` to `0.0.0.0` inside containers.
