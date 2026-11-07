// Provider verification — replays consumer pacts against the real API
// Run: start the provider on :3000, then npx jest provider.verify.test.js
const { Verifier } = require('@pact-foundation/pact');
const path = require('path');

describe('Pact Verification', () => {
  test('verifies pacts from the broker', async () => {
    const opts = {
      provider: 'user-service',
      providerBaseUrl: 'http://localhost:3000',
      // Local file mode:
      pactUrls: [
        path.resolve(__dirname, 'pacts', 'order-service-user-service.json'),
      ],
      // Broker mode (recommended — replace pactUrls):
      // pactBrokerUrl: process.env.PACT_BROKER_URL,
      // pactBrokerToken: process.env.PACT_BROKER_TOKEN,
      // consumerVersionSelectors: [{ tag: 'main', latest: true }],
      providerVersion: process.env.GIT_SHA || '1.0.0',
      // Provider state setup endpoint (see README):
      stateHandlers: {
        'a user with id 1 exists': () => testDb.insert({ id: 1, name: 'Alice' }),
        'no users exist': () => testDb.truncate('users'),
      },
    };

    await new Verifier(opts).verifyProvider();
  });
});
