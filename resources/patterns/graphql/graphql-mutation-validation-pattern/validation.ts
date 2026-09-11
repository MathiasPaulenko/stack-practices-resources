// validation.ts — GraphQL mutation validation framework.
// Run: npx ts-node validation.ts
// Requires: graphql (for GraphQLError)

export type ValidationRule = {
  field: string;
  rule: (value: any, input: Record<string, any>) => boolean;
  message: string;
  code: string;
};

export type ValidationError = {
  field: string;
  message: string;
  code: string;
};

/**
 * Validate input against a set of rules. Throws a structured error
 * with all field-level errors if any rule fails.
 *
 * Note: In production, throw a GraphQLError. For testing without the
 * graphql package, this throws a plain Error with the same shape.
 */
export function validateInput(
  input: Record<string, any>,
  rules: ValidationRule[],
): void {
  const errors: ValidationError[] = [];

  for (const rule of rules) {
    const value = input[rule.field];
    if (!rule.rule(value, input)) {
      errors.push({
        field: rule.field,
        message: rule.message,
        code: rule.code,
      });
    }
  }

  if (errors.length > 0) {
    const error: any = new Error("Validation failed");
    error.extensions = {
      code: "VALIDATION_ERROR",
      fields: errors.map((e) => e.field),
      errors,
      timestamp: new Date().toISOString(),
    };
    throw error;
  }
}

/**
 * Collect validation errors without throwing. Useful for testing
 * and for cases where you want to accumulate errors across multiple
 * validation passes.
 */
export function collectErrors(
  input: Record<string, any>,
  rules: ValidationRule[],
): ValidationError[] {
  const errors: ValidationError[] = [];
  for (const rule of rules) {
    const value = input[rule.field];
    if (!rule.rule(value, input)) {
      errors.push({
        field: rule.field,
        message: rule.message,
        code: rule.code,
      });
    }
  }
  return errors;
}
