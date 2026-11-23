# Observer Pattern — Companion Resources

Runnable versions of the observer pattern implementations from the
[Observer Pattern recipe](https://stackpractices.com/recipes/observer-pattern-recipe/)
on StackPractices.

## Files

| File | What it shows |
| --- | --- |
| `order-event-emitter.ts` | Basic typed event emitter for order lifecycle events (Node.js/TypeScript) |
| `typed-event-emitter.ts` | Compile-time safe emitter with an event map and per-listener error isolation |
| `debounced-event-emitter.ts` | Emitter that batches high-frequency events (e.g., keystrokes) into one notification |
| `weak-observer.ts` | Observer registry built on `WeakRef` so targets can be garbage-collected |
| `order-observer.java` | Observer with `PropertyChangeSupport`, the JDK's built-in mechanism |
| `reactive-orders.py` | Reactive streams with RxPY: subject, filtered and mapped subscriptions |

## Running

TypeScript files run with `ts-node`, `tsx`, or after compiling with `tsc`:

```bash
npx tsx order-event-emitter.ts
```

Java needs a JDK (11+):

```bash
javac order-observer.java && java OrderObserverDemo
```

Python needs RxPY:

```bash
pip install reactivex
python reactive-orders.py
```
