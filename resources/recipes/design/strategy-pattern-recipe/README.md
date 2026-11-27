# Strategy Pattern Recipe — Companion Code

Runnable examples from [Swap Algorithms at Runtime with the Strategy Pattern](https://stackpractices.com/recipes/strategy-pattern-recipe/) on StackPractices.

## Files

| File | What it shows |
|---|---|
| `shipping_strategy.ts` | Class-based `ShippingStrategy` interface with flat-rate, weight-based and distance-based implementations plus a `CheckoutService` context |
| `TaxStrategy.java` | Java enum strategy: `US`, `EU` and `UK` tax calculations behind a single `calculate` method |
| `function_strategies.py` | Python function strategies — plain callables dispatched by key, no classes needed |
| `strategy_registry.ts` | A generic `StrategyRegistry` that maps string keys to strategies selected at runtime |
| `pricing_decorators.ts` | Strategy composition: discount, tax and free-shipping decorators wrapping a base pricing strategy |
| `payment_context.py` | A `PaymentContext` that registers credit-card, PayPal and crypto strategies and dispatches by method name |

## Usage

- `.py` files run on Python 3.8+ with no dependencies.
- `.ts` files need TypeScript (`tsc` or `ts-node`); shared types like `Order` and `Money` are defined where used.
- `TaxStrategy.java` compiles standalone; add a `main` to run it.
