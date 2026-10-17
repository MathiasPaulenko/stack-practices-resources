# SOLID Principles Guide — Companion Resources

Companion code for the guide [SOLID Principles Explained with Examples](https://stackpractices.com/guides/solid-principles-guide/).

A before/after refactor of a TypeScript payment service showing all five SOLID principles applied to the same class.

## Contents

| Path | What it shows |
| --- | --- |
| `before/payment-processor.ts` | The legacy version: one method that validates, charges via a hardcoded Stripe client, logs, emails, and writes to a hardcoded MySQL connection. Violates SRP, OCP, and DIP. |
| `after/interfaces.ts` | The contracts: `PaymentValidator`, `PaymentGateway`, `PaymentRepository`, `NotificationService`, `Logger`. Narrow interfaces (ISP). |
| `after/implementations.ts` | Concrete implementations: `StripeGateway`, `PayPalGateway`, `PostgresPaymentRepository`, `EmailNotificationService`, `WinstonLogger`. One responsibility each (SRP); new gateways extend without modifying existing code (OCP). |
| `after/payment-processor.ts` | The refactored class: depends only on the interfaces (DIP), so any `PaymentGateway` can be substituted (LSP). |
| `after/composition.ts` | The composition root that wires abstractions to implementations, plus a fully mocked processor for tests — no patching framework needed. |

## How to use

1. Read `before/payment-processor.ts` and spot the violations.
2. Compare with the `after/` modules to see how each principle reshapes the code.
3. Swap `StripeGateway` for `PayPalGateway` in `after/composition.ts` — nothing else needs to change.
4. Use `testProcessor` as a starting point for unit tests with plain object mocks.
