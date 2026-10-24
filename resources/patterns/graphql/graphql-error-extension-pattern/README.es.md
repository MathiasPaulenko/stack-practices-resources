# Patrón de Extensión de Errores en GraphQL

Código de apoyo del [patrón de Extensión de Errores en GraphQL](https://stackpractices.com/es/patterns/graphql-error-extension-pattern/) en StackPractices.

## Archivos

| Archivo | Descripción |
| --- | --- |
| `error-codes.ts` | Enum compartido de códigos de error (`UNAUTHENTICATED`, `NOT_FOUND`, `VALIDATION_ERROR`, ...) |
| `extended-error.ts` | Clase `GraphQLExtendedError` que siempre adjunta `extensions.code` más metadatos extra |
| `resolvers.ts` | Resolvers de ejemplo de Query/Mutation lanzando errores estructurados |
| `format-error.ts` | Configuración `formatError` de Apollo Server que sanitiza errores y elimina stack traces |
| `client.ts` | Fetch del lado del cliente que ramifica según `extensions.code` |

Cada `.ts` tiene su equivalente `.js`.

## Setup

```bash
npm install graphql @apollo/server
```

## Uso

```typescript
import { ErrorCodes } from './error-codes';
import { GraphQLExtendedError } from './extended-error';
import { resolvers } from './resolvers';
import { createServer } from './format-error';

const server = createServer(typeDefs, resolvers);
```

Lanza `GraphQLExtendedError` en cualquier resolver y los clientes pueden ramificar
según `error.extensions.code` en lugar de parsear `error.message`.
