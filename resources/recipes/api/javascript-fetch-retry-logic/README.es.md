# Lógica de Reintento en JavaScript Fetch — Recursos Companion

Código companion de la receta [Lógica de Reintento en JavaScript Fetch con Backoff](https://stackpractices.com/es/recipes/javascript-fetch-retry-logic/) en StackPractices.

## Contenido

| Archivo | Descripción |
| --- | --- |
| `fetch_with_retry.js` | Reintento estilo función: backoff exponencial, jitter completo, `AbortSignal.timeout`/`any`, `Retry-After` |
| `fetch_retry_breaker.js` | Clase `FetchWithRetry` + `CircuitBreaker` que solo cuenta fallos de disponibilidad |
| `post_with_retry.js` | Reintentos POST seguros con un `Idempotency-Key` compartido |
| `fetch_retry.test.js` | Tests ejecutables (`node:test` + servidor mock de `node:http`, sin dependencias) |
| `package.json` | Config ESM + script `npm test` |

## Requisitos

- Node.js 18+ (incluye `fetch`, `AbortSignal.timeout`, `AbortSignal.any`). Recomendado Node 20+.

## Ejecutar los tests

```bash
npm test
# o directamente:
node --test
```

La suite levanta un servidor `node:http` real que devuelve 503/404/429 bajo demanda, así que ejercita la ruta de reintento sobre HTTP de verdad — incluido el manejo de `Retry-After` y el conteo del breaker. `baseDelay: 1` mantiene todo instantáneo.

## Uso

```javascript
import { fetchWithRetry } from "./fetch_with_retry.js";
import { FetchWithRetry } from "./fetch_retry_breaker.js";
import { postWithRetry } from "./post_with_retry.js";

const res = await fetchWithRetry("https://api.example.com/data");

const client = new FetchWithRetry({ retries: 4, breakerThreshold: 5 });
const res2 = await client.request("https://api.example.com/users");

const res3 = await postWithRetry("https://api.example.com/orders", { item: 42 });
```

## Notas

- Solo reintenta fallos de disponibilidad: 5xx, 429, errores de red, timeouts. Los 4xx se devuelven tal cual.
- En Node, `fetch` corre sobre undici — para una política de servicio completo, mira el `RetryHandler` de undici en lugar de envolver cada llamada.
- `Idempotency-Key` solo ayuda si el servidor deduplica con esa cabecera; revisa la doc de tu API antes de reintentar POSTs.
