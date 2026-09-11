# Auth a nivel campo con directivas GraphQL personalizadas

Código companion para la [receta de directivas de auth en GraphQL](https://stackpractices.com/es/recipes/graphql-directives-auth/) en StackPractices.

## Archivos

| Archivo | Descripción |
| --- | --- |
| `schema.ts` | Definiciones de tipos GraphQL con directivas `@auth`, `@owner` y `@hasPermission` |
| `directives/auth.ts` | Transformador de directiva de auth basada en roles con jerarquía |
| `directives/owner.ts` | Transformador de directiva de auth basada en propiedad |
| `directives/permission.ts` | Transformador de directiva de auth basada en permisos |
| `server.ts` | Configuración de Apollo Server con transformadores de directivas |
| `test_directives.test.ts` | Tests unitarios para la lógica de jerarquía de roles |

## Setup

```bash
npm install @apollo/server graphql @graphql-tools/schema @graphql-tools/utils graphql-tag
npm install -D vitest
```

## Ejecutar el servidor

```bash
npx tsx server.ts
```

## Ejecutar los tests

```bash
npx vitest run test_directives.test.ts
```

Los tests cubren la lógica de jerarquía de roles (función `hasRole`) sin requerir un servidor corriendo.

## Uso

```typescript
import { ApolloServer } from '@apollo/server';
import { makeExecutableSchema } from '@graphql-tools/schema';
import { authDirectiveTransformer } from './directives/auth';
import { ownerDirectiveTransformer } from './directives/owner';
import { typeDefs, resolvers } from './schema';

let schema = makeExecutableSchema({ typeDefs, resolvers });
schema = authDirectiveTransformer(schema);
schema = ownerDirectiveTransformer(schema);

const server = new ApolloServer({ schema });
```
