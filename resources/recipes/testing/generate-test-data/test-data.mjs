// Deterministic test data generators with @faker-js/faker.
//
// Usage:
//   npm install @faker-js/faker
//   node test-data.mjs

import { faker } from '@faker-js/faker';

faker.seed(12345); // deterministic across runs

// Field generators
console.log('name:', faker.person.fullName());
console.log('email:', faker.internet.email());
console.log('int 18-65:', faker.number.int({ min: 18, max: 65 }));

// Factory function with overrides
function createUser(overrides = {}) {
  return {
    id: faker.string.uuid(),
    name: faker.person.fullName(),
    email: faker.internet.email(),
    age: faker.number.int({ min: 18, max: 90 }),
    avatar: faker.image.avatar(),
    isActive: true,
    ...overrides,
  };
}

const user = createUser();
console.log('user:', user);

const batch = Array.from({ length: 5 }, () => createUser());
console.log('batch size:', batch.length);

// Domain-specific factory
const createOrder = (overrides = {}) => ({
  id: faker.string.uuid(),
  customerId: faker.string.uuid(),
  items: Array.from({ length: faker.number.int({ min: 1, max: 5 }) }, () => ({
    sku: `SKU-${faker.string.alphanumeric(6).toUpperCase()}`,
    quantity: faker.number.int({ min: 1, max: 10 }),
    price: faker.commerce.price({ min: 5, max: 500 }),
  })),
  status: faker.helpers.arrayElement(['pending', 'paid', 'shipped', 'delivered']),
  createdAt: faker.date.past(),
  ...overrides,
});

console.log('order:', createOrder());

// Deterministic data for snapshot tests
faker.seed(42);
console.log('snapshot user:', createUser({ name: 'Snapshot User' }));
