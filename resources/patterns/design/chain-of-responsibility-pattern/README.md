# Chain of Responsibility Pattern

Runnable companion code for the StackPractices pattern
[Chain of Responsibility Pattern](https://stackpractices.com/patterns/chain-of-responsibility-pattern/).

## Files

| File | What it shows |
| --- | --- |
| `src/chain.py` | Python: `Handler` ABC + `AuthHandler`/`RateLimitHandler`/`DataHandler` with fluent `set_next` chaining. |
| `src/chain.js` | JavaScript: same chain with `setNext` and `super.handle` forwarding. |
| `src/Chain.java` | Java: `Handler`/`passToNext` with `main` demo. |

## Usage

```bash
python src/chain.py   # Processed / 401 Unauthorized
node src/chain.js     # same output
javac src/Chain.java && java -cp src Chain
```

## Related

- Pattern page (EN): <https://stackpractices.com/patterns/chain-of-responsibility-pattern/>
- Pattern page (ES): <https://stackpractices.com/es/patterns/chain-of-responsibility-pattern/>
- Middleware variant: <https://stackpractices.com/patterns/chain-of-responsibility-middleware/>
