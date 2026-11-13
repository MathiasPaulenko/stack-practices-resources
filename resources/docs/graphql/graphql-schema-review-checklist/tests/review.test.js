import { describe, it, expect } from 'vitest';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';
import { reviewSchema } from '../review.mjs';

const here = dirname(fileURLToPath(import.meta.url));
const good = readFileSync(join(here, '../schemas/good-schema.graphqls'), 'utf-8');
const bad = readFileSync(join(here, '../schemas/bad-schema.graphqls'), 'utf-8');

describe('reviewSchema on good-schema', () => {
  it('passes all automated checks', () => {
    expect(reviewSchema(good)).toEqual([]);
  });
});

describe('reviewSchema on bad-schema', () => {
  const failures = reviewSchema(bad);
  const checks = new Set(failures.map((f) => f.check));

  it('flags non-PascalCase type names', () => {
    expect(checks.has('type-names-pascal')).toBe(true);
    expect(failures.some((f) => f.where === 'users')).toBe(true);
  });

  it('flags non-camelCase field names and String-typed id', () => {
    expect(failures.some((f) => f.where === 'users.first_name')).toBe(true);
    expect(failures.some((f) => f.check === 'id-uses-id-type')).toBe(true);
  });

  it('flags Boolean without verb prefix and lowercase enum values', () => {
    expect(checks.has('boolean-verb-prefix')).toBe(true);
    expect(failures.some((f) => f.where === 'Status.pending')).toBe(true);
  });

  it('flags missing pagination and offset usage', () => {
    expect(checks.has('list-needs-pagination')).toBe(true);
    expect(checks.has('no-offset-pagination')).toBe(true);
    expect(failures.some((f) => f.where === 'Query.allOrders')).toBe(true);
  });

  it('flags @deprecated without reason', () => {
    expect(failures.some((f) => f.where === 'Query.oldField' && f.check === 'deprecated-needs-reason')).toBe(true);
  });

  it('flags mutation shape violations', () => {
    expect(checks.has('mutation-verb')).toBe(true);
    expect(checks.has('mutation-single-input')).toBe(true);
    expect(checks.has('mutation-returns-payload')).toBe(true);
  });
});
