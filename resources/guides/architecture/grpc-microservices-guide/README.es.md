# Microservicios gRPC — Contrato, Servidor, Clientes, Envoy

Recursos companion de la guía [gRPC en Microservicios — Guía de RPC de Alto Rendimiento](https://stackpractices.com/es/guides/grpc-microservices-guide/).

## Archivos

| Archivo | Qué es |
| --- | --- |
| `user_service.proto` | Contrato proto3 — RPCs unary, server-streaming y bidireccional, listo para codegen |
| `server.py` | Servidor Python con health check `grpc.health.v1` y store en memoria |
| `client.py` | Cliente Python — unary + server streaming, deadlines de 5s, variante TLS en comentario |
| `client.go` | Cliente Go — API de credenciales post-1.40 (`insecure.NewCredentials()`), `context.WithTimeout` |
| `envoy.yaml` | Config L7 de Envoy — balanceo `LEAST_REQUEST` por RPC + health checks gRPC |
| `docker-compose.yml` | Lab local: 2 réplicas del servicio tras Envoy en :8080 |

## Inicio rápido

```bash
# 1. Genera los stubs de Python
pip install grpcio grpcio-tools grpcio-health-checking
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. user_service.proto

# 2. Levanta servidor + cliente
python server.py &
python client.py

# 3. O el lab completo con Envoy L7
docker compose up -d
grpcurl -plaintext localhost:8080 list
```

## Trampas

- `grpc.WithInsecure()` está deprecated en grpc-go — usa `insecure.NewCredentials()`.
- `insecure_channel` / credenciales insecure son solo para dev; en producción TLS o mTLS del mesh.
- El deadline por defecto de gRPC es infinito — pon `timeout`/`context.WithTimeout` en cada llamada.
- El balanceo TCP (L4) pega las conexiones HTTP/2 a un pod; necesitas Envoy/Linkerd o `round_robin` client-side.
