# Test Strategy Example: payments-service

Filled example of the test strategy template applied to a payments microservice.

## Context

```text
Service: payments-service
Team: 4 backend devs, 1 QA, 1 SRE
Stack: Node.js, PostgreSQL, RabbitMQ, Stripe API
```

## Test Pyramid

```text
Unit: 75% (120 tests, < 20s)
  - Total calculation logic, taxes, discounts
  - Request schema validation
  - Order state machine (pending -> paid -> refunded)
  - Currency formatting and rounding helpers

Integration: 18% (28 tests, < 4min)
  - POST /payments with real PostgreSQL (Testcontainers)
  - Stripe webhook with valid and invalid HMAC signature
  - Event publishing to RabbitMQ
  - Idempotency: same payment_intent_id does not create double charge

E2E: 5% (8 tests, < 10min)
  - Full flow: create order -> pay -> confirm -> refund
  - Error flow: payment declined -> user notification
  - Concurrency: two simultaneous payments for same order

Contract: 2% (4 tests, < 30s)
  - Contract with orders-service (consumer)
  - Contract with notifications-service (consumer)
```

## CI/CD Gates

```text
Pre-commit: lint + type check (15s)
  Gate: 0 errors
PR build: unit + integration + contract (5min)
  Gate: 100% pass, coverage >= 90% (payments is critical)
  Gate: no new flaky tests
Nightly: E2E + load baseline (25min)
  Gate: 95% pass, p95 < 300ms, no memory leaks
Pre-release: full load + soak (60min)
  Gate: 100% pass, SLOs met, no 5xx errors
```

## Specific Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Stripe API change | Low | Critical | Contract tests with Stripe sandbox |
| Webhook lost | Medium | High | Retry + nightly reconciliation |
| Double payment from retry | Medium | Critical | Idempotency key + DB unique constraint |
| Race condition on stock | High | High | SELECT FOR UPDATE in transaction |

## Test Data

- Factory: `createPayment()`, `createRefund()`, `createWebhookEvent()`
- Stripe sandbox: test keys, cards 4242, 4000, etc.
- DB: PostgreSQL in Testcontainer, isolated data per test
- RabbitMQ: in-memory instance or Testcontainer

## Tracked Metrics

- Coverage: 90% line, 85% branch (higher than general target)
- Defect escape rate: < 2 per sprint (payments is critical)
- p95 latency: < 300ms at baseline
- Flaky test rate: < 0.5% (stricter than general)
