// Apollo Server 4 wiring for ValidationException → VALIDATION_ERROR.
// Requires @apollo/server installed. Resolver errors reach formatError
// wrapped in GraphQLError, so unwrap before the instanceof check.
import { ApolloServer } from '@apollo/server';
import { unwrapResolverError } from '@apollo/server/errors';
import { typeDefs } from './schema.ts';
import { resolvers } from './resolvers.ts';
import { ValidationException } from './errors.ts';

export const server = new ApolloServer({
  typeDefs,
  resolvers,
  formatError: (formattedError, error) => {
    const unwrapped = unwrapResolverError(error);
    if (unwrapped instanceof ValidationException) {
      return {
        message: 'Input validation failed',
        extensions: {
          code: 'VALIDATION_ERROR',
          errors: unwrapped.validationErrors,
        },
      };
    }
    return formattedError;
  },
});
