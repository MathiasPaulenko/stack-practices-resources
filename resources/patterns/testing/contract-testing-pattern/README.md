# Contract Testing Pattern — Companion Code

Runnable artifacts for the [Contract Testing pattern](https://stackpractices.com/patterns/contract-testing-pattern/) on StackPractices.

## Files

| File | What it does |
|---|---|
| `consumer.pact.test.js` | Pact consumer test (Jest) — records interactions, uses matchers and a provider state, writes the pact file |
| `provider.verify.test.js` | Provider verification — replays pacts against the real API with `stateHandlers` for provider states |
| `consumer_pact_test.py` | The same consumer contract in pact-python / pytest style |
| `contract-tests.yml` | GitHub Actions workflow — consumer publishes pacts to the broker, provider verifies from it |
| `can-i-deploy.sh` | Release gate script — asks the broker whether a version is safe to deploy |

## Usage

```bash
# Consumer side (Node)
npm i @pact-foundation/pact jest
npx jest consumer.pact.test.js          # writes pacts/order-service-user-service.json

# Provider side: start the API on :3000, then
npx jest provider.verify.test.js

# Python consumer
pip install pact-python pytest
pytest consumer_pact_test.py

# Deploy gate
export PACT_BROKER_URL=... PACT_BROKER_TOKEN=... GIT_SHA=$(git rev-parse HEAD)
./can-i-deploy.sh order-service production
```

## Provider state setup

The verifier calls `stateHandlers` (or a `/pact-state-setup` endpoint) before each replay so the provider can put its test database into the condition the consumer described — e.g. `a user with id 1 exists`.

## Related

- Pattern: https://stackpractices.com/patterns/contract-testing-pattern/
- Recipe (runnable CI walkthrough): https://stackpractices.com/recipes/api-contract-testing/
- Pact docs: https://docs.pact.io/
