# Caching en GraphQL — Recurso Companion

Código companion de la guía de StackPractices [Guía completa de caching en GraphQL](https://stackpractices.com/es/guides/complete-guide-graphql-caching/).

## Contenidos

- `apollo-client-persisted-queries.js` — Apollo Client con persisted queries, GET requests y config de cache normalizado.
- `dataloader-with-redis.js` — DataLoader que verifica Redis primero, luego fall back a la base de datos.
- `cache-invalidation.js` — Invalidación de cache event-driven con Redis pub/sub y cache keys versionadas.
- `apollo-client-normalized-cache.js` — Cache normalizado de Apollo Client con helpers de actualización post-mutación.
- `meta.json` — Metadata del recurso.

## Ejecución

Estos son snippets de referencia, no una app runnable. Copiá el patrón relevante a tu setup de Apollo Server o Apollo Client.

## Conceptos clave

- **CDN caching**: GET requests + persisted queries para cache keys consistentes.
- **DataLoader**: batching y caching por request para prevenir N+1.
- **Redis**: caching cross-request con TTL y pub/sub para invalidación.
- **Apollo Client**: cache normalizado con actualizaciones post-mutación.
- **Invalidación de cache**: event-driven, keys versionadas y purging basado en tags.
