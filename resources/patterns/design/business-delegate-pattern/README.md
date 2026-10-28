# Business Delegate Pattern

Companion code for the pattern [Business Delegate Pattern](https://stackpractices.com/patterns/business-delegate-pattern/).

## Contents

| File | What it is |
|------|------------|
| `order_delegate.py` | Full delegate chain in Python: `ServiceLocator`, cached reference, `OrderBusinessDelegate`, `ResilientOrderDelegate` with retry + backoff, and a controller demo |
| `OrderBusinessDelegate.java` | Classic J2EE-style delegate with nested lookup and exception translation, runnable `main` |
| `order-delegate.js` | JavaScript delegate with `Map`-based service locator and cached reference |

## How to use

- Python: `python order_delegate.py` — stdlib only.
- JavaScript: `node order-delegate.js`.
- Java: `javac OrderBusinessDelegate.java && java OrderBusinessDelegate`.

Each file mirrors a section of the pattern page: service lookup via `ServiceLocator`, cached service references, exception translation, and the resilient variant with retry and backoff.
