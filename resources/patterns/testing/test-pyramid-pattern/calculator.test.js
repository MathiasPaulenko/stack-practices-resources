// calculator.test.js — Vitest / Jest
// Run: npx vitest run calculator.test.js
import { describe, it, expect } from 'vitest';
import { parsePrice, applyDiscount } from './pricing.js';

describe('parsePrice', () => {
  it('parses a valid decimal price', () => {
    expect(parsePrice('19.99')).toBe(19.99);
  });

  it('rejects non-numeric input', () => {
    // toThrow accepts an Error class, an instance, or a message substring
    expect(() => parsePrice('abc')).toThrow('Invalid price');
  });

  it('rejects negative prices', () => {
    expect(() => parsePrice('-5')).toThrow('Invalid price');
  });
});

describe('applyDiscount', () => {
  it('applies a percentage discount', () => {
    expect(applyDiscount(100, 0.1)).toBeCloseTo(90);
  });

  it('never returns a negative total', () => {
    expect(applyDiscount(50, 1.5)).toBe(0);
  });
});
