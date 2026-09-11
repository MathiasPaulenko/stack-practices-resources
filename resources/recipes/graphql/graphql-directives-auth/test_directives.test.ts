// test_directives.test.ts — Unit tests for auth and owner directive logic
// Run with: npx vitest run test_directives.test.ts
import { describe, it, expect } from 'vitest';
import { hasRole } from './roleHierarchy';

describe('hasRole', () => {
  it('ADMIN satisfies ADMIN requirement', () => {
    expect(hasRole('ADMIN', 'ADMIN')).toBe(true);
  });

  it('ADMIN satisfies EDITOR requirement (hierarchy)', () => {
    expect(hasRole('ADMIN', 'EDITOR')).toBe(true);
  });

  it('ADMIN satisfies VIEWER requirement (hierarchy)', () => {
    expect(hasRole('ADMIN', 'VIEWER')).toBe(true);
  });

  it('EDITOR satisfies EDITOR requirement', () => {
    expect(hasRole('EDITOR', 'EDITOR')).toBe(true);
  });

  it('EDITOR satisfies VIEWER requirement (hierarchy)', () => {
    expect(hasRole('EDITOR', 'VIEWER')).toBe(true);
  });

  it('EDITOR does NOT satisfy ADMIN requirement', () => {
    expect(hasRole('EDITOR', 'ADMIN')).toBe(false);
  });

  it('VIEWER satisfies VIEWER requirement', () => {
    expect(hasRole('VIEWER', 'VIEWER')).toBe(true);
  });

  it('VIEWER does NOT satisfy EDITOR requirement', () => {
    expect(hasRole('VIEWER', 'EDITOR')).toBe(false);
  });

  it('VIEWER does NOT satisfy ADMIN requirement', () => {
    expect(hasRole('VIEWER', 'ADMIN')).toBe(false);
  });

  it('unknown role does NOT satisfy any requirement', () => {
    expect(hasRole('GUEST', 'VIEWER')).toBe(false);
  });

  it('any role does NOT satisfy unknown requirement', () => {
    expect(hasRole('ADMIN', 'SUPERADMIN')).toBe(false);
  });
});
