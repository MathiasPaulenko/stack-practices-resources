# SOLID Principles TypeScript — Order Service Companion

Companion code for [SOLID Principles in TypeScript](https://stackpractices.com/patterns/solid-principles-typescript/).

The order-service scenario from the pattern, as runnable TypeScript:

- **SRP** — `OrderValidator`, `OrderRepository`, `OrderNotifier` each own one job
- **OCP** — new discounts are new `DiscountStrategy` classes, not edits
- **LSP** — any `DiscountStrategy` works wherever another does
- **ISP** — `Readable`/`Writable` split so consumers depend only on what they use
- **DIP** — `OrderService` takes interfaces via constructor injection

## Run the tests

```bash
npm install vitest typescript
npx vitest run
```

Versión en español: [README.es.md](README.es.md)
