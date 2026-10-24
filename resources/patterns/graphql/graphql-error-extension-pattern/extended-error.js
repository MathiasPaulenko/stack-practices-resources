import { GraphQLError } from 'graphql';

/**
 * GraphQLError subclass that always attaches `extensions.code`
 * plus any extra metadata clients need (field, http.status, retryAfter...).
 */
export class GraphQLExtendedError extends GraphQLError {
  constructor(message, code, extensions = {}) {
    super(message, {
      extensions: {
        code,
        ...extensions,
      },
    });
  }
}
