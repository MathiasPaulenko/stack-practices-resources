# gRPC API Companion — Runnable Examples

Companion repository for [gRPC API with Protocol Buffers](https://stackpractices.com/recipes/grpc-api/).

## Files

| File | Language | Description |
| ------ | ---------- | ------------- |
| `service.proto` | Protocol Buffers | Shared schema for Greeter service |
| `server.py` | Python | gRPC server with unary and streaming RPC |
| `client.py` | Python | gRPC client (unary + streaming) |
| `server.js` | JavaScript | gRPC server with @grpc/grpc-js |
| `client.js` | JavaScript | gRPC client (unary + streaming) |
| `Server.java` | Java | gRPC server with Netty transport |
| `Client.java` | Java | gRPC client (unary + streaming) |

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

Compile with Maven using `pom.xml`. Generate stubs from `service.proto` using
`protoc` with the `grpc-java` plugin. Run `Server.java` then `Client.java`.
