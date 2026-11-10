# Domain-Driven Design Tactical Patterns — Companion Files

Runnable examples for the recipe on
[stackpractices.com](https://stackpractices.com/recipes/domain-driven-design/).

## Files

- `money.ts` — `Money` value object: immutable, self-validating, currency-safe math
- `order_aggregate.py` — `Order` aggregate root with `OrderPlaced` domain events
- `order_repository.py` — repository + Unit of Work + application service (in-memory, runs without a DB)
- `pricing_service.ts` — domain service for cross-aggregate pricing
- `specifications.ts` — composable `Specification<T>` with and/or/not
- `OrderToShipmentAdapter.java` — anti-corruption layer translating Order → Shipping (illustrative)

## Quick start

```bash
# Python aggregate + repository pipeline (stdlib only)
python order_aggregate.py
python order_repository.py
```

```bash
# TypeScript files need a TS runtime (ts-node, bun, or tsc)
npx ts-node money.ts
```
