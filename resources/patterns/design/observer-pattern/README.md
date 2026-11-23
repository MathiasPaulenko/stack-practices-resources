# Observer Pattern — Companion Resources

Runnable implementations of the Observer pattern from the [StackPractices guide](https://stackpractices.com/patterns/observer-pattern/):

| File | Language | What it shows |
|------|----------|---------------|
| `observer.py` | Python 3 | Subject with attach/notify and unsubscribe callables |
| `observer.js` | JavaScript | `Set`-based observer list, error isolation per observer |
| `Subject.java` | Java | Typed `Observer` interface, `Runnable` unsubscribe |
| `event-emitter.ts` | TypeScript | Per-event channels with `Map<string, Set<Observer>>` |

Every `subscribe`/`attach` returns an unsubscribe handle — call it in teardown to avoid the classic observer memory leak. Each `notify`/`emit` wraps observer calls so one failing observer can't break the rest.

## Run

```bash
python observer.py
node observer.js
javac Subject.java && java Subject
npx tsx event-emitter.ts   # or ts-node
```
