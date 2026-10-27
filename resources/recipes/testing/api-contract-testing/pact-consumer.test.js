// Consumer contract test with Pact V3.
// Run: npm test -- pact-consumer.test.js
// Requires: npm install @pact-foundation/pact
const { PactV3 } = require('@pact-foundation/pact');
const { like, regex } = require('@pact-foundation/pact').MatchersV3;

const provider = new PactV3({
  consumer: 'order-service',
  provider: 'user-service',
  dir: 'pacts',
});

describe('User Service Contract', () => {
  test('returns user by ID', async () => {
    await provider
      .given('user with id 123 exists')
      .uponReceiving('a request for user 123')
      .withRequest({
        method: 'GET',
        path: '/users/123',
      })
      .willRespondWith({
        status: 200,
        body: {
          id: like(123),
          name: like('Alice'),
          email: regex(/^[^\s@]+@[^\s@]+\.[^\s@]+$/, 'alice@example.com'),
        },
      });

    await provider.executeTest(async (mockServer) => {
      const user = await fetchUser(mockServer.url, 123);
      expect(user.name).toBe('Alice');
    });
  });
});

// Async message pact: consumer declares the event shape it depends on.
const { MessageConsumerPact } = require('@pact-foundation/pact');

describe('Inventory Events Contract', () => {
  test('stock.updated event has the expected shape', async () => {
    const messagePact = new MessageConsumerPact({
      consumer: 'order-service',
      provider: 'inventory-events',
      dir: 'pacts',
    });

    await messagePact
      .given('inventory was updated')
      .expectsToReceive('a stock.updated event')
      .withContent({ sku: like('ABC-123'), quantity: like(5) })
      .verify(async (message) => {
        expect(message.contents.sku).toBe('ABC-123');
      });
  });
});
