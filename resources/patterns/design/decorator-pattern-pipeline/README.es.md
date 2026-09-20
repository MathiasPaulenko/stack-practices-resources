# Patrón Decorator para pipelines de peticiones HTTP — Código complementario

Código complementario de [Patrón Decorator en pipelines HTTP](https://stackpractices.com/es/patterns/decorator-pattern-pipeline/) en StackPractices.

## Qué contiene

| Archivo | Rol |
|---------|-----|
| `src/HttpClient.ts` | Interfaz compartida que implementa cada capa |
| `src/FetchClient.ts` | Cliente más interno — wrapper fino sobre `fetch` |
| `src/BaseClientDecorator.ts` | Base abstracta que guarda la referencia al `HttpClient` interno |
| `src/LoggingDecorator.ts` | Registra método, URL, estado y tiempo |
| `src/RetryDecorator.ts` | Reintentos selectivos: comprueba `response.ok`, solo 502/503/504 + errores de red, backoff exponencial con jitter |
| `src/AuthDecorator.ts` | Inyecta el header `Authorization: Bearer` en cada petición, incluidos los reintentos |
| `src/CircuitBreakerDecorator.ts` | Máquina de estados cerrado → abierto → half-open; petición de prueba tras `resetTimeout` |
| `src/httpClientFactory.ts` | `createHttpClient(config)` construye el stack completo |
| `demo.ts` | Ejecuta un GET contra JSONPlaceholder a través de todo el stack |

## Ejecutarlo

Requiere Node 20+ (fetch nativo) y `tsx` o `ts-node`:

```bash
npx tsx demo.ts
```

Salida esperada:

```text
GET https://jsonplaceholder.typicode.com/todos/1 → 200 (XXXms)
status: 200
body: { userId: 1, id: 1, title: 'delectus aut autem', completed: false }
```

## Detalles clave

- `fetch` resuelve ante errores HTTP — `RetryDecorator` comprueba `response.ok` y solo reintenta 502/503/504 más fallos de red.
- Orden de decoradores en la factory: `Auth → Retry → Logging → CircuitBreaker → Fetch`. Auth en la capa más externa para que los reintentos lleven el token; el circuit breaker en la más interna para ver los fallos de red reales.
- Cada decorador clona `options` antes de mutar los headers, así que los reintentos no acumulan estado duplicado.
