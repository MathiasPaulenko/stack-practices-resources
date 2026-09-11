# Field-Level Auth with Custom GraphQL Directives

Companion code for the [GraphQL directives auth recipe](https://stackpractices.com/recipes/graphql-directives-auth/) on StackPractices.

## Files

| File | Description |
| --- | --- |
| `schema.ts` | GraphQL type definitions with `@auth`, `@owner`, and `@hasPermission` directives |
| `directives/auth.ts` | Role-based auth directive transformer with hierarchy |
| `directives/owner.ts` | Ownership-based auth directive transformer |
| `directives/permission.ts` | Permission-based auth directive transformer |
| `server.ts` | Apollo Server setup with directive transformers registered |
| `test_directives.test.ts` | Unit tests for role hierarchy logic |

## Setup

```bash
npm install @apollo/server graphql @graphql-tools/schema @graphql-tools/utils graphql-tag
npm install -D vitest
```

## Running the Server

```bash
npx tsx server.ts
```

## Running the Tests

```bash
npx vitest run test_directives.test.ts
```

The tests cover the role hierarchy logic (`hasRole` function) without requiring a running server.

## Usage

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
