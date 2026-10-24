/**
 * Shared error-code enum for the GraphQL Error Extension pattern.
 * Keep these strings stable after release: clients branch on them.
 */
export const ErrorCodes = {
  UNAUTHENTICATED: 'UNAUTHENTICATED',
  FORBIDDEN: 'FORBIDDEN',
  NOT_FOUND: 'NOT_FOUND',
  VALIDATION_ERROR: 'VALIDATION_ERROR',
  BAD_USER_INPUT: 'BAD_USER_INPUT',
  INTERNAL_ERROR: 'INTERNAL_ERROR',
  RATE_LIMITED: 'RATE_LIMITED',
  CONFLICT: 'CONFLICT',
};
