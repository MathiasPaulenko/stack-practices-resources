# Gateway de GraphQL Federation — Demo ejecutable de dos subgrafos

Companion ejecutable de la receta [Configura un gateway de GraphQL Federation con Apollo](https://stackpractices.com/es/recipes/graphql-federation-gateway-setup/).

## Qué demuestra

- Dos subgrafos reales con `buildSubgraphSchema`: users posee `User @key`, posts extiende `User` con `@external`
- Composición de supergrafo con `IntrospectAndCompose` al arrancar el gateway
- Una consulta real entre subgrafos: `posts { author { name posts } }` resuelve `name` mediante una llamada `_entities` al subgrafo de users y `posts` de vuelta en el subgrafo de posts
- Resolución de entidades con `__resolveReference` en acción

## Ejecutar

```bash
npm install
npm start
```

El demo levanta users en :4001, posts en :4002 y el gateway en :4000, ejecuta la consulta federada, imprime la respuesta JSON unida y verifica que `author.name` vino del subgrafo de users.

## Archivos

| Archivo | Propósito |
| --- | --- |
| `src/users-service.ts` | Subgrafo dueño de `User` con `__resolveReference` |
| `src/posts-service.ts` | Subgrafo dueño de `Post`, extendiendo `User` vía `@extends`/`@external` |
| `src/gateway.ts` | `ApolloGateway` + `IntrospectAndCompose` + context |
| `src/demo.ts` | Levanta los tres servicios, ejecuta la consulta federada, imprime la prueba |
