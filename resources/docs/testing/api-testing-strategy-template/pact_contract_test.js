// Pact contract test — consumer verifies the provider honors the pact
const { Pact } = require('@pact-foundation/pact');

const provider = new Pact({
  consumer: 'mobile-app',
  provider: 'orders-api',
  port: 1234,
});

describe('Orders API contract', () => {
  beforeAll(() => provider.setup());
  afterAll(() => provider.finalize());

  it('returns an order with the expected shape', async () => {
    await provider.addInteraction({
      state: 'order 123 exists',
      uponReceiving: 'a request for order 123',
      withRequest: { method: 'GET', path: '/orders/123' },
      willRespondWith: {
        status: 200,
        body: { id: '123', status: 'shipped', total: expect.any(Number) },
      },
    });
    const res = await api.getOrder('123');
    expect(res.body.status).toBe('shipped');
  });
});
