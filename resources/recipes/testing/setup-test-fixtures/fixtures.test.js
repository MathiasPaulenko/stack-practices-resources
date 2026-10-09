// Jest fixture patterns: beforeAll/afterAll for suite state,
// beforeEach for per-test resets, factories for object graphs.
//
// Usage: npm install --save-dev jest && npx jest fixtures.test.js

import { createUser, resetCounter } from './factories.js';

const canAccessAdmin = (user) => user.role === 'admin';

let sharedDb;

beforeAll(() => {
  // expensive setup once per suite
  sharedDb = { tables: [], connected: true };
});

afterAll(() => {
  sharedDb.connected = false;
});

beforeEach(() => {
  // mutable state reset before every test
  sharedDb.tables.length = 0;
});

describe('fixture lifecycle', () => {
  test('admin can access admin panel', () => {
    const admin = createUser({ role: 'admin' });
    expect(canAccessAdmin(admin)).toBe(true);
  });

  test('viewer cannot access admin panel', () => {
    const viewer = createUser({ role: 'viewer' });
    expect(canAccessAdmin(viewer)).toBe(false);
  });

  test('state reset between tests', () => {
    sharedDb.tables.push('users');
    expect(sharedDb.tables).toHaveLength(1); // second run sees 0 thanks to beforeEach
  });
});

describe('deterministic factories', () => {
  beforeEach(() => resetCounter());

  test('ids are sequential and predictable', () => {
    const a = createUser();
    const b = createUser();
    expect(b.id).toBe(a.id + 1);
  });
});
