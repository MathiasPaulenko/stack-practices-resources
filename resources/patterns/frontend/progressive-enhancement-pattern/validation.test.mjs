import { test } from 'node:test';
import assert from 'node:assert/strict';
import { validateValue } from './validation.mjs';

test('required field rejects empty and whitespace-only values', () => {
  assert.equal(validateValue({ value: '', required: true }).isValid, false);
  assert.equal(validateValue({ value: '   ', required: true }).isValid, false);
  assert.equal(validateValue({ value: 'Alice', required: true }).isValid, true);
});

test('email type validates format only when a value is present', () => {
  assert.equal(validateValue({ value: '', type: 'email' }).isValid, true);
  assert.equal(validateValue({ value: 'not-an-email', type: 'email' }).isValid, false);
  assert.equal(validateValue({ value: 'alice@example.com', type: 'email' }).isValid, true);
});

test('maxLength rejects oversized values', () => {
  assert.equal(validateValue({ value: 'x'.repeat(101), maxLength: 100 }).isValid, false);
  assert.equal(validateValue({ value: 'x'.repeat(100), maxLength: 100 }).isValid, true);
});

test('valid input returns an empty message', () => {
  const result = validateValue({ value: 'ok', required: true, maxLength: 10 });
  assert.equal(result.isValid, true);
  assert.equal(result.message, '');
});
