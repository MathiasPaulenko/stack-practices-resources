# Microservice Contract Template

Companion pack for [Microservice Contract Template](https://stackpractices.com/docs/microservice-contract-template/) on StackPractices.

## Files

- `contract-template.md` — copy-paste contract template (parties, API spec, endpoints, SLA, versioning, breaking changes, error handling, escalation)
- `contract-filled-example.md` — the same template filled in for `checkout-web` ↔ `payments-service`
- `pact-consumer.test.js` — Pact consumer-driven contract test (needs `@pact-foundation/pact`)
- `openapi-fragment.yaml` — minimal OpenAPI 3.1 fragment to link from the contract
- `user-service.proto` — proto3 contract; check compatibility with `buf breaking --against ".git#branch=main"`

## Usage

1. Copy `contract-template.md` next to your provider's code (or into a central `contracts/` repo).
2. Fill in every placeholder — real Slack channels and a concrete sunset date, not generic text.
3. Wire enforcement: run the Pact test in the consumer CI, `buf breaking` for protobuf, OpenAPI diffs on spec changes.
