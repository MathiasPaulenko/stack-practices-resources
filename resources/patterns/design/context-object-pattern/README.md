# Context Object Pattern — Companion Code

Runnable implementations for the [context-object-pattern article](https://stackpractices.com/patterns/context-object-pattern/) on StackPractices.

## Files

| File | Language | What it shows |
|------|----------|---------------|
| `context_object.py` | Python 3.10+ | `frozen` dataclass + `replace()` for immutable copies |
| `context-object.js` | Node.js 18+ | `Object.freeze` context built in the handler |
| `ContextObjectDemo.java` | Java 11+ | Immutable context with a builder |

## Run

```bash
python context_object.py     # → "context-object-pattern OK"
node context-object.js       # → "context-object-pattern OK"
javac ContextObjectDemo.java && java ContextObjectDemo   # → "context-object-pattern OK"
```

Each demo builds a `RequestContext` once in the request handler (the boundary), passes it through the service layer, and returns an order id — no threading of request metadata through every signature.
