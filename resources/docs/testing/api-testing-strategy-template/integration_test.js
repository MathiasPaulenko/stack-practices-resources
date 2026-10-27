// Integration test — supertest against the real app + test DB (Testcontainers)
const request = require('supertest');
const app = require('../app');

describe('POST /orders', () => {
  it('creates an order and returns 201', async () => {
    const res = await request(app)
      .post('/orders')
      .send({ sku: 'ABC', qty: 2 });
    expect(res.status).toBe(201);
    expect(res.body.id).toBeDefined();
  });

  it('rejects duplicate idempotency key with 409', async () => {
    const res = await request(app)
      .post('/orders')
      .set('Idempotency-Key', 'dup-1')
      .send({ sku: 'ABC', qty: 2 });
    expect(res.status).toBe(409);
  });
});
