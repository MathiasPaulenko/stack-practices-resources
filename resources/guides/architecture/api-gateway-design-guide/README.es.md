# Diseño de API Gateway — Ejemplo de Pipeline de Middleware

Ejemplo ejecutable en TypeScript para la [guía de diseño de API Gateway](https://stackpractices.com/es/guides/api-gateway-design-guide/) de StackPractices.

Un pipeline de gateway mínimo que compone las cuatro capas de middleware de la guía — autenticación, rate limiting, caché de respuestas y circuit breaker — delante de un router de prefijos sin estado. Sin Express, sin Redis, sin librería JWT: tipos agnósticos de framework más `node:crypto` para verificación HS256.

## Estructura

```text
pipeline/        types.ts (Request/Response/Middleware) + gateway.ts (composición)
middleware/      auth.ts (JWT + cabeceras de identidad)
                 rateLimit.ts (token bucket, store intercambiable)
                 cache.ts (caché GET con claves por usuario)
                 circuitBreaker.ts (closed/open/half-open)
routing/         router.ts (enrutamiento por prefijo, stripPrefix opcional)
stores/          InMemoryTokenBucketStore, InMemoryResponseCache
upstream/        StubUpstream (doble de test scriptable)
tests/           Tests Jest que cubren el pipeline completo
```

## Cómo funciona

`createGateway(middlewares, router)` reduce la lista de middleware sobre el router para que `auth → rateLimit → cache → circuitBreaker → router` se ejecute en orden — la misma secuencia del diagrama de pipeline de la guía (la terminación TLS queda fuera, en el load balancer).

1. `authMiddleware` verifica el JWT, inyecta `x-user-id`/`x-user-roles`/`x-user-scopes` para los upstreams y corta con 401.
2. `rateLimitMiddleware` rellena un token bucket por identidad a través de un `TokenBucketStore` — cambia `InMemoryTokenBucketStore` por una implementación Redis y todas las réplicas comparten la cuota.
3. `cacheMiddleware` cachea respuestas GET con la identidad del llamante en la clave y respeta el `Cache-Control: max-age` del upstream.
4. `circuitBreakerMiddleware` falla rápido tras N errores consecutivos del upstream y solo deja pasar un número limitado de sondas en half-open.
5. `createRouter` casa por prefijo; `stripPrefix` reescribe `/api/users/42` a `/42` antes de reenviar.

## Ejecutar los tests

Los suites no necesitan servicios externos — todos los stores están en memoria y el upstream es un stub scriptable:

```bash
npm install -D typescript ts-jest @types/jest jest
npx jest tests/
```

## Conectarlo de verdad

Sustituye las piezas en memoria en la raíz de composición: un `TokenBucketStore` sobre Redis, el adaptador de tu framework traduciendo HTTP a `GatewayRequest` y funciones `Upstream` reales por ruta. Los contratos de middleware se mantienen idénticos — ese es el punto de mantenerlos agnósticos de framework.
