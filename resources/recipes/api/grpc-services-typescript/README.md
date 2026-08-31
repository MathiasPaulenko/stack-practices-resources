# gRPC TypeScript Services

Companion project for [Build gRPC Services in TypeScript with Protocol Buffers](https://stackpractices.com/recipes/grpc-services-typescript/).

This example shows how to build a gRPC server and client in TypeScript using `@grpc/grpc-js`, Protocol Buffers and `grpc-health-check`. It covers unary, server streaming, client streaming, bidirectional streaming, health checks, metadata propagation, deadlines and TLS.

## Requirements

- Node.js 20+
- `npm`
- OpenSSL (only if you want to try TLS locally)

## Setup

```bash
npm install
npm run proto:generate
```

The command above generates the TypeScript stubs from `proto/user.proto` and places them in `generated/`.

## Run in development (insecure)

In one terminal:

```bash
npm run start:server
```

In another terminal:

```bash
npm run start:client
```

To verify health:

```bash
npm run start:health
```

## Run with TLS

Generate self-signed certificates:

```bash
mkdir -p certs
openssl req -x509 -newkey rsa:4096 -keyout certs/server-key.pem -out certs/server-cert.pem -days 365 -nodes -subj "/CN=localhost"
openssl req -x509 -newkey rsa:4096 -keyout certs/ca-key.pem -out certs/ca-cert.pem -days 365 -nodes -subj "/CN=My Local CA"
```

Run the server and client with TLS enabled:

```bash
GRPC_TLS=true npm run start:server
GRPC_TLS=true npm run start:client
```

Do not commit the `certs/` folder.

## Project structure

```text
proto/user.proto          # Protocol Buffers contract
generated/                # Generated JS/TS stubs (after npm run proto:generate)
src/server.ts             # gRPC server with all four call types and health checks
src/client.ts             # gRPC client with interceptor, deadlines and streaming
src/health-client.ts      # Standalone health-check client
package.json
tsconfig.json
.env.example
```
