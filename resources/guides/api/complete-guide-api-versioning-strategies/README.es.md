# Estrategias de Versionado de APIs — Companion

Ejemplos ejecutables de la [Guía Completa de Estrategias de Versionado de APIs](https://stackpractices.com/es/guides/complete-guide-api-versioning-strategies/).

## Archivos

- `uri_versioning.py` — routers v1/v2 montados por prefijo de ruta
- `query_param_versioning.py` — dispatch por `?version=` con default explícito
- `header_versioning.py` — dispatch por header `X-API-Version`
- `content_negotiation.py` — versionado por media type `Accept: application/vnd.*+json`
- `graphql_additive.graphql` / `graphql_deprecation.graphql` — evolución aditiva y `@deprecated`
- `graphql_schemas.js` — esquemas paralelos / opciones por directivas
- `deprecation_headers.py` — headers `Deprecation` + `Sunset` + `Link` sucesor
- `strangler_fig_router.py` — router fachada que proxea endpoints migrados a v2
- `parallel_run.py` — comparador shadow-run que loguea mismatches v1/v2

## Uso

Requiere `fastapi`, `httpx` (ejemplos Python), `graphql` (ejemplo JS). Copia el router de la estrategia elegida a tu app.
