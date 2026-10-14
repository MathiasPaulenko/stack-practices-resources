// Jest — nested describes, factory functions, beforeEach/afterEach
// Run: npx jest jest_fixtures.test.js

function createTestUser(overrides = {}) {
  return {
    id: 1,
    name: 'Alice',
    email: 'alice@x.com',
    role: 'member',
    createdAt: new Date('2026-01-01'),
    ...overrides,
  };
}

function createTestOrder(overrides = {}) {
  return {
    id: 100,
    userId: 1,
    items: [
      { productId: 1, quantity: 2, price: 10.0 },
      { productId: 2, quantity: 1, price: 25.0 },
    ],
    status: 'pending',
    total: 45.0,
    ...overrides,
  };
}

class OrderService {
  constructor() {
    this.orders = new Map();
  }
  createOrder(data) {
    this.orders.set(data.id || 100, { status: 'pending', ...data });
    return this.orders.get(data.id || 100);
  }
  getOrder(id) { return this.orders.get(id); }
  cancel(id) {
    const o = this.orders.get(id);
    if (o.status !== 'pending') throw new Error('InvalidStateError');
    o.status = 'cancelled';
  }
  complete(id) { this.orders.get(id).status = 'completed'; }
  calculateTotal(order, user) {
    const base = (order.items || []).reduce((s, i) => s + i.price * i.quantity, 0);
    if (base === 0) throw new Error('EmptyOrderError');
    return user && user.role === 'premium' ? base * 0.9 : base;
  }
}

describe('OrderService', () => {
  let service;

  beforeEach(() => {
    service = new OrderService();
  });

  test('calculates order total', () => {
    const order = createTestOrder({ items: [{ productId: 1, quantity: 3, price: 15.0 }] });
    expect(service.calculateTotal(order)).toBe(45.0);
  });

  test('rejects empty order', () => {
    const order = createTestOrder({ items: [] });
    expect(() => service.calculateTotal(order)).toThrow('EmptyOrderError');
  });

  test('applies discount for premium user', () => {
    const user = createTestUser({ role: 'premium' });
    const order = createTestOrder({ userId: user.id });
    expect(service.calculateTotal(order, user)).toBe(40.5);
  });

  describe('with pending order', () => {
    let order;

    beforeEach(() => {
      order = service.createOrder({ id: 1, userId: 1, total: 100 });
    });

    test('can be cancelled', () => {
      service.cancel(order.id);
      expect(service.getOrder(order.id).status).toBe('cancelled');
    });

    test('can be completed', () => {
      service.complete(order.id);
      expect(service.getOrder(order.id).status).toBe('completed');
    });
  });

  describe('with completed order', () => {
    beforeEach(() => {
      service.createOrder({ id: 1, userId: 1, total: 100 });
      service.complete(1);
    });

    test('cannot be cancelled', () => {
      expect(() => service.cancel(1)).toThrow('InvalidStateError');
    });
  });
});
