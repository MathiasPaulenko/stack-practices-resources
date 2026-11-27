import { describe, expect, it } from 'vitest';
import { byAgeThenName, numericAsc, nullsLast } from './sort-examples.js';

describe('sort examples', () => {
  it('sorts numbers numerically, not lexicographically', () => {
    expect(numericAsc([10, 2, 1])).toEqual([1, 2, 10]);
  });

  it('sorts by age then name', () => {
    const users = [
      { name: 'Bob', age: 30 },
      { name: 'Ada', age: 30 },
      { name: 'Chen', age: 25 },
    ];
    expect(byAgeThenName(users).map((u) => u.name)).toEqual(['Chen', 'Ada', 'Bob']);
  });

  it('pushes nulls to the end', () => {
    expect(nullsLast([3, null, 1])).toEqual([1, 3, null]);
  });
});
