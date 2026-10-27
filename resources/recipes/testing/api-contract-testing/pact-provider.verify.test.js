// Provider verification: replays published consumer contracts against the real API.
// Run: npm test -- pact-provider.verify.test.js
// Requires: npm install @pact-foundation/pact and a running provider on :3000
const { Verifier } = require('@pact-foundation/pact');

describe('Pact Verification', () => {
  test('validates against consumer contracts', async () => {
    await new Verifier({
      provider: 'user-service',
      providerBaseUrl: 'http://localhost:3000',
      pactBrokerUrl: process.env.PACT_BROKER_URL,
      pactBrokerToken: process.env.PACT_BROKER_TOKEN,
      publishVerificationResult: true,
      providerVersion: process.env.GIT_SHA,
      providerBranch: process.env.GIT_BRANCH,
      // Every given(...) in a consumer pact needs a matching state handler.
      // Miss one and verification fails with "missing provider state".
      stateHandlers: {
        'user with id 123 exists': async () => {
          await seedUser({ id: 123, name: 'Alice', email: 'alice@example.com' });
        },
      },
    }).verifyProvider();
  });
});
