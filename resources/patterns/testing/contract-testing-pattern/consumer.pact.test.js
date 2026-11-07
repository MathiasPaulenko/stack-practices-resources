// Consumer contract test — order-service vs user-service
// Run: npx jest consumer.pact.test.js
// Produces: pacts/order-service-user-service.json
const { Pact, MatchersV3 } = require('@pact-foundation/pact');
const path = require('path');

const { like, eachLike, term } = MatchersV3;

const provider = new Pact({
  consumer: 'order-service',
  provider: 'user-service',
  port: 8080,
  log: path.resolve(__dirname, 'logs', 'pact.log'),
  dir: path.resolve(__dirname, 'pacts'),
});

describe('User Service Contract', () => {
  beforeAll(() => provider.setup());
  afterAll(() => provider.finalize());
  afterEach(() => provider.verify());

  test('GET /users/:id returns user', async () => {
    await provider.addInteraction({
      state: 'a user with id 1 exists',
      uponReceiving: 'a request for a user',
      withRequest: {
        method: 'GET',
        path: '/users/1',
        headers: { Accept: 'application/json' },
      },
      willRespondWith: {
        status: 200,
        headers: { 'Content-Type': 'application/json' },
        body: {
          id: like(1),
          name: like('Alice'),
          email: like('alice@x.com'),
          role: term({ generate: 'admin', matcher: 'admin|member|guest' }),
        },
      },
    });

    const user = await getUser(1); // your client hitting http://localhost:8080
    expect(user.name).toBe('Alice');
  });

  test('GET /users returns a list', async () => {
    await provider.addInteraction({
      uponReceiving: 'a request for all users',
      withRequest: {
        method: 'GET',
        path: '/users',
        query: { page: '1', per_page: '20' },
      },
      willRespondWith: {
        status: 200,
        body: {
          data: eachLike({
            id: like(1),
            name: like('Alice'),
            email: like('alice@x.com'),
          }),
          pagination: { page: like(1), per_page: like(20), total: like(100) },
        },
      },
    });

    const response = await getUsers({ page: 1, perPage: 20 });
    expect(response.data.length).toBeGreaterThan(0);
  });
});
