import { PactV3 } from '@pact-foundation/pact';

const pact = new PactV3({
  consumer: 'OrderFrontend',
  provider: 'OrderAPI',
});

describe('Order API contract', () => {
  it('returns order details', async () => {
    await pact
      .given('an order exists')
      .uponReceiving('a request for order details')
      .withRequest({
        method: 'GET',
        path: '/orders/123',
        headers: { Accept: 'application/json' },
      })
      .willRespondWith({
        status: 200,
        headers: { 'Content-Type': 'application/json' },
        body: {
          id: pact.like('123'),
          status: pact.like('pending'),
          total: pact.like(99.99),
        },
      });

    await pact.executeTest(async (mockServer) => {
      const response = await fetch(`${mockServer.url}/orders/123`);
      const data = await response.json();
      expect(data.status).toBe('pending');
    });
  });
});
