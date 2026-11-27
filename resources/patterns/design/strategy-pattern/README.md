# Strategy Pattern — Companion Code

Runnable examples from [Strategy Pattern: Interchangeable Algorithms at Runtime](https://stackpractices.com/patterns/strategy-pattern/) on StackPractices.

## Files

| File | What it shows |
|---|---|
| `payment_strategy.py` | Abstract `PaymentStrategy` interface with credit card and PayPal implementations, plus a `Checkout` context |
| `strategy_checkout.js` | The same payment strategies as plain JavaScript classes — no interface needed |
| `StrategyCheckout.java` | Java `interface` + implementations + `Checkout` with `setStrategy` |
| `pricing_strategy.ts` | Full pricing service: regular/member/senior/holiday strategies plus a `CompositePricing` that stacks them |

## Usage

- `payment_strategy.py` runs on Python 3.8+ with no dependencies.
- `strategy_checkout.js` runs on any modern Node.js.
- `StrategyCheckout.java` compiles standalone; add a `main` to run it.
- `pricing_strategy.ts` needs TypeScript (`tsc` or `ts-node`).
