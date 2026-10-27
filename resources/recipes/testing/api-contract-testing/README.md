# API Contract Testing — Companion Resources

Companion files for the [Test API Contracts with Consumer-Driven Contracts](https://stackpractices.com/recipes/api-contract-testing/) recipe on StackPractices.com.

## What's included

| File | Format | Description |
|------|--------|-------------|
| `pact-consumer.test.js` | JavaScript | Pact V3 consumer test (HTTP) plus an async `MessageConsumerPact` example for event-driven contracts |
| `pact-provider.verify.test.js` | JavaScript | Provider `Verifier` setup with `stateHandlers` that seed data for each `given(...)` state |
| `openapi-validate.py` | Python | Provider-driven check: validates the OpenAPI spec, then unmarshals a live response against it |
| `contract-testing-ci.yml` | YAML | GitHub Actions pipeline: pact verification on every PR plus a `can-i-deploy` deploy gate |

## Quick start

### 1. Install dependencies

```bash
npm install --save-dev @pact-foundation/pact
pip install openapi-spec-validator openapi-core requests
```

### 2. Run the consumer test

```bash
npm test -- pact-consumer.test.js
```

This writes the pact files to `pacts/`. Publish them to your Pact Broker with `pact-broker publish pacts/`.

### 3. Verify the provider

With the provider running on port 3000:

```bash
export PACT_BROKER_URL=https://your-broker
export PACT_BROKER_TOKEN=...
export GIT_SHA=$(git rev-parse HEAD)
export GIT_BRANCH=$(git branch --show-current)

npm test -- pact-provider.verify.test.js
```

### 4. Gate the deploy

Drop `contract-testing-ci.yml` into `.github/workflows/` and set the `PACT_BROKER_URL` and `PACT_BROKER_TOKEN` secrets. `can-i-deploy` blocks the release whenever a consumer contract is unverified or failing for that version.
