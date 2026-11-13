// errors/codes.ts + errors/base.ts from the recipe, merged into one file.

import { GraphQLError } from 'graphql';

export const ErrorCodes = {
  VALIDATION_ERROR: 'VALIDATION_ERROR',
  UNAUTHENTICATED: 'UNAUTHENTICATED',
  FORBIDDEN: 'FORBIDDEN',
  NOT_FOUND: 'NOT_FOUND',
  CONFLICT: 'CONFLICT',
  RATE_LIMITED: 'RATE_LIMITED',
} as const;

export type ErrorCode = (typeof ErrorCodes)[keyof typeof ErrorCodes];

export class AppError extends GraphQLError {
  constructor(message: string, code: ErrorCode, extensions?: Record<string, unknown>) {
    super(message, { extensions: { code, ...extensions } });
  }
}

export class ValidationError extends AppError {
  constructor(errors: { field: string; message: string }[]) {
    super('Input validation failed', ErrorCodes.VALIDATION_ERROR, { errors });
  }
}

export class AuthenticationError extends AppError {
  constructor(message = 'Authentication required') {
    super(message, ErrorCodes.UNAUTHENTICATED);
  }
}

export class ForbiddenError extends AppError {
  constructor(message = 'Insufficient permissions', requiredRole?: string) {
    super(message, ErrorCodes.FORBIDDEN, { requiredRole });
  }
}

export class NotFoundError extends AppError {
  constructor(resource: string, id: string) {
    super(`${resource} not found`, ErrorCodes.NOT_FOUND, { resource, id });
  }
}

export class ConflictError extends AppError {
  constructor(message: string, conflicts?: Record<string, unknown>) {
    super(message, ErrorCodes.CONFLICT, { conflicts });
  }
}
