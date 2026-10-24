import { ApolloServer } from '@apollo/server';

/**
 * Apollo Server config with a sanitizing formatError.
 * Never leaks stack traces or internal details to clients.
 */
export function createServer(typeDefs, resolvers) {
  return new ApolloServer({
    typeDefs,
    resolvers,
    formatError: (formattedError, error) => {
      // Never expose internal errors to clients
      if (formattedError.extensions?.code === 'INTERNAL_ERROR') {
        return {
          message: 'An internal error occurred',
          extensions: {
            code: 'INTERNAL_ERROR',
            timestamp: new Date().toISOString(),
          },
        };
      }

      // Log full error server-side, return sanitized version to client
      console.error('GraphQL Error:', {
        code: formattedError.extensions?.code,
        message: formattedError.message,
        path: formattedError.path,
        stack: error?.stack,
      });

      // Remove stack traces from client responses
      delete formattedError.extensions?.stacktrace;
      return formattedError;
    },
  });
}
