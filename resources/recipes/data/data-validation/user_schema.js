// Joi user validation schema — run with: npm install joi && node user_schema.js
const Joi = require('joi');

const userSchema = Joi.object({
  email: Joi.string().email().required(),
  age: Joi.number().integer().min(18).max(120).required(),
  role: Joi.string().valid('user', 'admin', 'moderator').required(),
  tags: Joi.array().items(Joi.string()).max(10),
});

const { error, value } = userSchema.validate({
  email: 'a@b.com', age: 30, role: 'admin', tags: [],
});

if (error) {
  console.error('Invalid:', error.details.map(d => d.message));
  process.exit(1);
}
console.log('Valid user:', value.email, value.role);

const bad = userSchema.validate({ email: 'not-an-email', age: 10, role: 'x' });
console.log('Rejects bad input:', Boolean(bad.error));
