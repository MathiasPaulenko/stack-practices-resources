# Manejo de errores GraphQL — Demo de códigos de extensión estructurados

Companion ejecutable de la receta [Errores GraphQL estructurados con códigos de extensión](https://stackpractices.com/es/recipes/graphql-error-handling-best-practices/).

## Qué demuestra

- Subclases de `AppError` que llevan `extensions.code` más contexto (`errors`, `retryAfter`, `resource`, `requiredRole`)
- `formatError` de Apollo Server 4: los errores deliberados pasan intactos; las excepciones inesperadas llegan ya normalizadas a `INTERNAL_SERVER_ERROR`, donde el callback enmascara el mensaje filtrado y registra la causa real con `unwrapResolverError`
- Respuestas JSON reales para `UNAUTHENTICATED`, `FORBIDDEN`, `NOT_FOUND`, `VALIDATION_ERROR`, `CONFLICT` y el error interno enmascarado
- Ejecución in-process vía `server.executeHTTPGraphQLRequest`, sin abrir puertos

## Ejecutar

```bash
npm install
npm start
```

El demo ejecuta siete casos contra una instancia real de `ApolloServer` e imprime el status, los códigos de error y el body JSON completo de cada uno.

## Archivos

| Archivo | Propósito |
| --- | --- |
| `src/errors.ts` | Enum `ErrorCodes` + clase base `AppError` y errores especializados |
| `src/schema.ts` | `typeDefs` + resolvers sobre un store de posts en memoria |
| `src/server.ts` | `ApolloServer` con el enmascarado `formatError` de la receta |
| `src/demo.ts` | Siete casos de petición impresos como respuestas JSON reales |
