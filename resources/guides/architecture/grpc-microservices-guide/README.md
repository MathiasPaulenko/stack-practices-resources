# gRPC Microservices — Contract, Server, Clients, Envoy

Companion resources for the guide [gRPC in Microservices — High-Performance RPC Guide](https://stackpractices.com/guides/grpc-microservices-guide/).

## Files

| File | What it is |
| --- | --- |
| `user_service.proto` | proto3 contract — unary, server-streaming and bidirectional RPCs, ready for codegen |
| `server.py` | Python server with `grpc.health.v1` health check and in-memory store |
| `client.py` | Python client — unary + server streaming, 5s deadlines, TLS variant in comment |
| `client.go` | Go client — post-1.40 credentials API (`insecure.NewCredentials()`), `context.WithTimeout` |
| `envoy.yaml` | L7 Envoy config — per-RPC `LEAST_REQUEST` balancing + gRPC health checks |
| `docker-compose.yml` | Local lab: 2 service replicas behind Envoy on :8080 |

## Quick start

```bash
# 1. Generate Python stubs
pip install grpcio grpcio-tools grpcio-health-checking
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. user_service.proto

# 2. Run server + client
python server.py &
python client.py

# 3. Or the full lab with Envoy L7 LB
docker compose up -d
grpcurl -plaintext localhost:8080 list
```

## Gotchas

- `grpc.WithInsecure()` is deprecated in grpc-go — use `insecure.NewCredentials()`.
- `insecure_channel` / insecure credentials are dev-only; production needs TLS or mesh mTLS.
- gRPC default deadline is infinite — set `timeout`/`context.WithTimeout` on every call.
- TCP (L4) load balancing pins HTTP/2 connections to one pod; you need Envoy/Linkerd or client-side `round_robin`.
