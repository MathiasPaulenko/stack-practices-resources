# Plantilla de Contrato de Microservicios

Pack complementario de [Plantilla de Contrato de Microservicios](https://stackpractices.com/es/docs/microservice-contract-template/) en StackPractices.

## Archivos

- `contract-template.md` — plantilla de contrato lista para copiar (partes, spec de API, endpoints, SLA, versionado, cambios incompatibles, manejo de errores, escalamiento)
- `contract-filled-example.md` — la misma plantilla rellenada para `checkout-web` ↔ `payments-service`
- `pact-consumer.test.js` — test de contrato orientado al consumidor con Pact (requiere `@pact-foundation/pact`)
- `openapi-fragment.yaml` — fragmento mínimo de OpenAPI 3.1 para enlazar desde el contrato
- `user-service.proto` — contrato proto3; comprueba compatibilidad con `buf breaking --against ".git#branch=main"`

## Uso

1. Copia `contract-template.md` junto al código del proveedor (o a un repo central `contracts/`).
2. Rellena cada placeholder — canales de Slack reales y una fecha de cierre concreta, no texto genérico.
3. Conecta el enforcement: ejecuta el test de Pact en el CI del consumidor, `buf breaking` para protobuf y diffs de OpenAPI en cambios de spec.
