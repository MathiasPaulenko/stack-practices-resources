/**
 * Input validation — runnable Zod example.
 *
 * Schema-first validation: declare the shape once, use safeParse to
 * collect every violation as field-level errors.
 *
 * Run:  node validate_user.js   (requires: npm install)
 */

const { z } = require('zod');

const UserCreate = z.object({
  name: z.string().trim().min(1, 'name cannot be blank').max(100),
  email: z.string().email(),
  age: z.number().int().min(0).max(150),
  bio: z.string().max(500).optional(),
});

/** Turn a ZodError into field-level error objects for a 400 response. */
function formatErrors(error) {
  return error.issues.map((issue) => ({
    field: issue.path.join('.'),
    message: issue.message,
    code: issue.code,
  }));
}

/** Parse and return { data } or { errors } — never throws. */
function validateUser(payload) {
  const result = UserCreate.safeParse(payload);
  return result.success ? { data: result.data } : { errors: formatErrors(result.error) };
}

module.exports = { UserCreate, validateUser, formatErrors };

if (require.main === module) {
  console.log('valid:', validateUser({ name: 'Ada Lovelace', email: 'ada@example.com', age: 36 }));
  console.log('invalid:', validateUser({ name: '  ', email: 'not-an-email', age: 200 }));
}
