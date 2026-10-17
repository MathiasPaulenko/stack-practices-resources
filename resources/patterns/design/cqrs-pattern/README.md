# CQRS Pattern — Companion Resources

Companion code for [CQRS Pattern](https://stackpractices.com/patterns/cqrs-pattern/).

Runnable demos of Command Query Responsibility Segregation in three languages, plus an event-driven projection demo showing the async variant.

## Contents

| File | What it shows |
| --- | --- |
| `cqrs_demo.py` | Command handler + query handler on a shared in-memory store, with invariant enforcement on the write side and a denormalized `OrderSummary` DTO on the read side. Run: `python cqrs_demo.py`. |
| `cqrs-demo.js` | Same command/query split in JavaScript. Run: `node cqrs-demo.js`. |
| `CqrsDemo.java` | Typed Java version with `record Item`, invariant in `Order.confirm()`, and a `main` that compiles standalone: `javac CqrsDemo.java && java CqrsDemo`. |
| `projection-demo.js` | The async variant: commands emit events to a log, a projection consumer rebuilds the read model. Demonstrates idempotent consumers and full replay (rebuild). Run: `node projection-demo.js`. |

## How to use

1. Run the three single-store demos first — that's "simple CQRS".
2. Then run `projection-demo.js` to see how events + projections replace synchronous sync when the stores split.
3. Experiment: add a second read model shape to `projection-demo.js` to see how projections multiply — and why consolidation matters.
