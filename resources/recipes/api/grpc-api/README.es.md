# Repositorio Companion de gRPC — Ejemplos Ejecutables

Repositorio companion para [API gRPC con Protocol Buffers](https://stackpractices.com/es/recipes/grpc-api/).

## Archivos

| Archivo | Lenguaje | Descripción |
| --------- | ---------- | ------------- |
| `service.proto` | Protocol Buffers | Esquema compartido del servicio Greeter |
| `server.py` | Python | Servidor gRPC con RPC unario y streaming |
| `client.py` | Python | Cliente gRPC (unario + streaming) |
| `server.js` | JavaScript | Servidor gRPC con @grpc/grpc-js |
| `client.js` | JavaScript | Cliente gRPC (unario + streaming) |
| `Server.java` | Java | Servidor gRPC con transporte Netty |
| `Client.java` | Java | Cliente gRPC (unario + streaming) |

## Python

```bash
pip install -r requirements.txt
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. service.proto
python server.py   # terminal 1
python client.py   # terminal 2
```

## JavaScript

```bash
npm install
node server.js   # terminal 1
node client.js   # terminal 2
```

## Java

Compila con Maven usando `pom.xml`. Genera los stubs desde `service.proto`
usando `protoc` con el plugin `grpc-java`. Ejecuta `Server.java` y luego `Client.java`.
