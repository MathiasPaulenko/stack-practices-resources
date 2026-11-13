import type { FieldError } from './schemas.ts';

export class ValidationException extends Error {
  readonly validationErrors: FieldError[];

  constructor(validationErrors: FieldError[]) {
    super('Validation failed');
    this.name = 'ValidationException';
    this.validationErrors = validationErrors;
  }
}
