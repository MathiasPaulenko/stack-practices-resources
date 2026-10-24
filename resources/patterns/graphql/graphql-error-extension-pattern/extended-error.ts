import { GraphQLError } from 'graphql';
import type { ErrorCode } from './error-codes';

/**
 * GraphQLError subclass that always attaches `extensions.code`
 * plus any extra metadata clients need (field, http.status, retryAfter...).
 */
export class GraphQLExtendedError extends GraphQLError {
  constructor(
    message: string,
    code: ErrorCode,
    extensions: Record<string, unknown> = {}
  ) {
    super(message, {
      extensions: {
        code,
        ...extensions,
      },
    });
  }
}
