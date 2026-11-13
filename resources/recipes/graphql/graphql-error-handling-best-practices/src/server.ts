// server.ts — ApolloServer instance with the recipe's formatError.

import { ApolloServer } from '@apollo/server';
import { ApolloServerErrorCode, unwrapResolverError } from '@apollo/server/errors';
import { resolvers, typeDefs, type Context } from './schema.js';

export function createServer() {
  return new ApolloServer<Context>({
    typeDefs,
    resolvers,
    includeStacktraceInErrorResponses: process.env.NODE_ENV !== 'production',
    formatError: (formattedError, error) => {
      // Deliberate errors carry our own code: let them through untouched.
      if (formattedError.extensions?.code !== ApolloServerErrorCode.INTERNAL_SERVER_ERROR) {
        return formattedError;
      }

      // Apollo already normalized this to INTERNAL_SERVER_ERROR, but the
      // original message still leaks. Mask it and log the real error.
      console.error('Unhandled resolver error:', unwrapResolverError(error));
      return {
        message: 'Internal server error',
        extensions: { code: ApolloServerErrorCode.INTERNAL_SERVER_ERROR },
      };
    },
  });
}
