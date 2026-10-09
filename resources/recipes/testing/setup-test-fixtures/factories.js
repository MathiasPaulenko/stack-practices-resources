// Shared factory helpers — deterministic IDs, per-test overrides.

let counter = 0;

export function createUser(overrides = {}) {
  counter += 1;
  return {
    id: counter,
    name: `user_${counter}`,
    email: `user_${counter}@test.com`,
    role: 'user',
    ...overrides,
  };
}

export function createOrder(overrides = {}) {
  counter += 1;
  return {
    id: counter,
    customerId: overrides.customerId ?? counter,
    items: [],
    status: 'pending',
    ...overrides,
  };
}

// Reset between suites if tests depend on counter state
export function resetCounter() {
  counter = 0;
}
