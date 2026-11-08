# Decorator Pattern — Runnable Implementations

Companion to the StackPractices pattern [Decorator Pattern](https://stackpractices.com/patterns/decorator-pattern/).

A decorator stack demo in three equivalent implementations: a `Coffee` component wrapped by `Milk`, `Sugar` and `Whip` decorators. Each decorator adds its own cost and label while delegating the rest of the call to the wrapped object. Stdlib only — no dependencies needed.

## Files

| File | Stack | Run |
| --- | --- | --- |
| `src/decorator_stack.py` | Python 3.9+ (stdlib only) | `python src/decorator_stack.py` |
| `src/decorator-stack.js` | Node.js 14+ (stdlib only) | `node src/decorator-stack.js` |
| `src/DecoratorStack.java` | Java 11+ | `javac -d src src/DecoratorStack.java && java -cp src DecoratorStack` |

Each run prints the plain component, a full stack (milk -> sugar -> whip), the same decorators reordered, and a free composition (double milk) — showing that decorators combine at runtime in any order and that the caller only ever sees the `Coffee` interface.

The example uses the classic coffee scenario so it maps 1:1 to the article; the same structure powers Java's I/O streams, Python's `@decorator` functions, and HTTP middleware pipelines.
