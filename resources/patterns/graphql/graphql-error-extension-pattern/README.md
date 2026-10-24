# GraphQL Error Extension Pattern

Companion code for the [GraphQL Error Extension pattern](https://stackpractices.com/patterns/graphql-error-extension-pattern/) on StackPractices.

## Files

| File | Description |
| --- | --- |
| `error-codes.ts` | Shared error-code enum (`UNAUTHENTICATED`, `NOT_FOUND`, `VALIDATION_ERROR`, ...) |
| `extended-error.ts` | `GraphQLExtendedError` class that always attaches `extensions.code` plus extra metadata |
| `resolvers.ts` | Example Query/Mutation resolvers throwing structured errors |
| `format-error.ts` | Apollo Server `formatError` config that sanitizes errors and strips stack traces |
| `client.ts` | Client-side fetch that branches on `extensions.code` |

Each `.ts` file has a `.js` equivalent.

## Setup

```bash
npm install graphql @apollo/server
```

## Usage

```typescript
import { ErrorCodes } from './error-codes';
import { GraphQLExtendedError } from './extended-error';
import { resolvers } from './resolvers';
import { createServer } from './format-error';

const server = createServer(typeDefs, resolvers);
```

Throw `GraphQLExtendedError` anywhere in a resolver and clients can switch on
`error.extensions.code` instead of parsing `error.message`.
