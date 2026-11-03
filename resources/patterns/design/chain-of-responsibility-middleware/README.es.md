# Chain of Responsibility — Pipeline de Middleware

Código ejecutable complementario del patrón de StackPractices
[Chain of Responsibility en Middleware de Peticiones](https://stackpractices.com/es/patterns/chain-of-responsibility-middleware/).

Ambas implementaciones simulan una petición HTTP que cruza
auth → rate limit → validación → logging antes de llegar al handler del
endpoint. Cualquier eslabón puede cortocircuitar la cadena — un token
inválido devuelve 401 sin tocar el resto de la pipeline.

## Archivos

| Archivo | Qué muestra |
| --- | --- |
| `src/middleware-chain.js` | Cadena de handlers basada en clases (`MiddlewareHandler`, `setNext`, `canHandle`, `process`). Ejecuta tres peticiones de demo: un POST que pasa, una petición rechazada sin token y un GET que omite la validación. |
| `src/express-compose.js` | `compose()` al estilo Express/Koa: el mismo bucle `dispatch(i)` que usa `koa-compose`, incluida la guarda de doble `next()`. |
| `src/middleware-chain.ts` | Versión TypeScript tipada de la cadena basada en clases. |
| `src/AuthFilter.java` | Variante con la API Servlet de Java: `FilterChain.doFilter()` es el `next()` del patrón; no llamarlo cortocircuita la cadena. |

## Uso

```bash
node src/middleware-chain.js   # demo de la cadena de clases
node src/express-compose.js    # demo del dispatch de compose()
npx tsx src/middleware-chain.ts  # versión TypeScript (necesita tsx o ts-node)
```

Salida esperada del primer archivo:

```text
Request 1: authenticated POST (passes every link)
  auth        -> user user123
  rate limit  -> 1/100 for cli-1
  validation  -> body ok
  logging     -> ... POST /orders
  endpoint    -> 200 OK for /orders

Request 2: missing token (auth short-circuits)
  chain error -> 401 Unauthorized

Request 3: GET skips validation but crosses auth/rate-limit/logging
  auth        -> user user123
  rate limit  -> 1/100 for user123
  logging     -> ... GET /orders
  endpoint    -> 200 OK for /orders
```

Fíjate en que el rate limiter cuenta `cli-1` en la petición 1 y `user123`
en la 3 — el eslabón de auth ya ha fijado `req.user.id` para entonces, que es
el orden de fallback de client ID (`x-client-id` → `req.user.id` →
`anonymous`) que describe el artículo.

## Relacionados

- Página del patrón (ES): <https://stackpractices.com/es/patterns/chain-of-responsibility-middleware/>
- Página del patrón (EN): <https://stackpractices.com/patterns/chain-of-responsibility-middleware/>
- Patrón genérico: <https://stackpractices.com/es/patterns/chain-of-responsibility-pattern/>
