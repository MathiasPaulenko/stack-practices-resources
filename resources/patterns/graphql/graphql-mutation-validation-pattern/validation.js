// validation.js — GraphQL mutation validation framework (JS version).

function validateInput(input, rules) {
  const errors = [];
  for (const rule of rules) {
    const value = input[rule.field];
    if (!rule.rule(value, input)) {
      errors.push({ field: rule.field, message: rule.message, code: rule.code });
    }
  }
  if (errors.length > 0) {
    const error = new Error("Validation failed");
    error.extensions = {
      code: "VALIDATION_ERROR",
      fields: errors.map(e => e.field),
      errors,
      timestamp: new Date().toISOString(),
    };
    throw error;
  }
}

function collectErrors(input, rules) {
  const errors = [];
  for (const rule of rules) {
    const value = input[rule.field];
    if (!rule.rule(value, input)) {
      errors.push({ field: rule.field, message: rule.message, code: rule.code });
    }
  }
  return errors;
}

module.exports = { validateInput, collectErrors };
