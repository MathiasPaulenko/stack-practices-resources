const { test } = require('node:test');
const assert = require('node:assert/strict');
const { validateUser } = require('./validate_user.js');

test('valid input returns data', () => {
  const { data, errors } = validateUser({ name: 'Ada Lovelace', email: 'ada@example.com', age: 36 });
  assert.equal(errors, undefined);
  assert.equal(data.name, 'Ada Lovelace');
});

test('blank name is rejected after trim', () => {
  const { errors } = validateUser({ name: '   ', email: 'ada@example.com', age: 36 });
  assert.ok(errors.some((e) => e.field === 'name'));
});

test('invalid email is rejected', () => {
  const { errors } = validateUser({ name: 'Ada', email: 'not-an-email', age: 36 });
  assert.ok(errors.some((e) => e.field === 'email'));
});

test('age bounds are enforced', () => {
  assert.ok(validateUser({ name: 'A', email: 'a@b.co', age: -1 }).errors);
  assert.ok(validateUser({ name: 'A', email: 'a@b.co', age: 151 }).errors);
});

test('all violations are aggregated', () => {
  const { errors } = validateUser({ name: '', email: 'bad', age: 999 });
  const fields = errors.map((e) => e.field);
  assert.ok(fields.includes('name'));
  assert.ok(fields.includes('email'));
  assert.ok(fields.includes('age'));
});
