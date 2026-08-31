# gRPC Services en TypeScript

Proyecto companion de [Construye servicios gRPC en TypeScript con Protocol Buffers](https://stackpractices.com/recipes/grpc-services-typescript/).

Este ejemplo muestra cómo construir un servidor y un cliente gRPC en TypeScript usando `@grpc/grpc-js`, Protocol Buffers y `grpc-health-check`. Cubre llamadas unarias, server streaming, client streaming, streaming bidireccional, health checks, propagación de metadata, deadlines y TLS.

## Requisitos

- Node.js 20+
- `npm`
- OpenSSL (solo si querés probar TLS localmente)

## Configuración

```bash
npm install
npm run proto:generate
```

El comando anterior genera los stubs de TypeScript desde `proto/user.proto` y los coloca en `generated/`.

## Correr en desarrollo (inseguro)

En una terminal:

```bash
npm run start:server
```

En otra terminal:

```bash
npm run start:client
```

Para verificar health:

```bash
npm run start:health
```

## Correr con TLS

Generá certificados self-signed:

```bash
mkdir -p certs
openssl req -x509 -newkey rsa:4096 -keyout certs/server-key.pem -out certs/server-cert.pem -days 365 -nodes -subj "/CN=localhost"
openssl req -x509 -newkey rsa:4096 -keyout certs/ca-key.pem -out certs/ca-cert.pem -days 365 -nodes -subj "/CN=My Local CA"
```

Corré el servidor y el cliente con TLS habilitado:

```bash
GRPC_TLS=true npm run start:server
GRPC_TLS=true npm run start:client
```

No comitees la carpeta `certs/`.

## Estructura del proyecto

```text
proto/user.proto          # Contrato de Protocol Buffers
generated/                # Stubs JS/TS generados (después de npm run proto:generate)
src/server.ts             # Servidor gRPC con los cuatro tipos de llamada y health checks
src/client.ts             # Cliente gRPC con interceptor, deadlines y streaming
src/health-client.ts      # Cliente de health-check standalone
package.json
tsconfig.json
.env.example
```
