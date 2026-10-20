# Module Pattern — Companion Examples

Runnable examples for the [Module Pattern](https://stackpractices.com/patterns/module-pattern/) on StackPractices.

## Contents

| File | Variant | Run |
|------|---------|-----|
| `iife-counter.js` | IIFE closure (pre-ES6 style) | `node iife-counter.js` |
| `esm-counter.js` + `esm-main.js` | ES module | `node esm-main.js` |
| `counter.py` | Python module (`_private` convention) | `python counter.py` |
| `Counter.java` | Java static class | `javac Counter.java && java com.myapp.counter.Counter` |
| `payment-module.ts` | Payment scenario with lifecycle + private state | `npx tsx payment-module.ts` |

## Notes

- Every variant keeps `count`/`log` private and exposes only `increment`, `decrement`, `getCount` — same contract, four mechanisms.
- Module state is shared state: every importer sees the same `count`. For independent instances you want a factory or class, not a module.
- Migrating an IIFE to an ES module: hoist the body to top level, drop the wrapper, replace the returned object with `export`s.

## Related

- [Singleton Pattern](https://stackpractices.com/patterns/singleton-pattern/)
- [Facade Pattern](https://stackpractices.com/patterns/facade-pattern/)
