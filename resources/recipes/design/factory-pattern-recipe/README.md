# Factory Pattern Recipe — Companion Resources

Code examples from the recipe [Create Objects Flexibly with the Factory Pattern](https://stackpractices.com/recipes/factory-pattern-recipe/).

## Files

| File | What it shows |
|------|---------------|
| `notification-factory.ts` | Factory Method: `NotificationFactory` subclasses pick `EmailNotifier`/`SmsNotifier` at runtime (TypeScript) |
| `payment-factory.py` | Simple Factory: `PaymentProcessorFactory.create("stripe")` returns the right `PaymentProcessor`, config via env vars (Python — runs standalone) |
| `UIFactoryDemo.java` | Abstract Factory: `WindowsUIFactory`/`MacUIFactory` produce consistent widget families (Java — `javac` + `java` runnable) |
| `di-container.ts` | Minimal DI container with `bind`/`resolve` factory providers and singleton caching (TypeScript) |
| `notification-builder.ts` | Factory + Builder combo: builder picks the channel and wraps the product in a `ResilientNotifier` retry policy (TypeScript) |
| `async-db-factory.py` | Async factory with lazy, lock-guarded `asyncpg` connection pooling (Python — needs a live PostgreSQL) |

## Notes

- `payment-factory.py` and `UIFactoryDemo.java` run standalone. The TypeScript files assume `tsx`/ESM top-level await; `async-db-factory.py` needs `pip install asyncpg` and PostgreSQL.
- Secrets come from environment variables with dev fallbacks — never hardcode credentials in factories.
