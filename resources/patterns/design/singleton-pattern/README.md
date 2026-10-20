# Singleton Pattern — runnable examples

Companion to the article: https://stackpractices.com/patterns/singleton-pattern/

Four ways to get exactly one instance, across languages — each file runs standalone and prints an assertion result.

| File | Language | Approach |
|------|----------|----------|
| `singleton.py` | Python | `__new__` guarded with `threading.Lock`, plus the `__init__` re-run trap handled |
| `connection_pool.py` | Python | Module-level singleton — the idiomatic Python way |
| `Configuration.java` | Java | Enum singleton — thread-safe, serialization- and reflection-proof |
| `CacheClient.java` | Java | Double-checked locking with `volatile` |
| `Registry.java` | Java | Bill Pugh holder idiom + `readResolve()` for serialization |
| `registry.ts` | TypeScript | Named registry / Multiton with `reset()` for tests |

## Run

```bash
python singleton.py            # Python 3.8+
python connection_pool.py

javac Configuration.java && java Configuration
javac CacheClient.java && java CacheClient
javac Registry.java && java Registry

npx ts-node registry.ts        # or: npx tsc registry.ts && node registry.js
```

## Which one should I use?

- **Java**: enum first (immune to everything), Bill Pugh if you need a real class, DCL only for configurable lazy init — never without `volatile`.
- **Python**: module-level instance; avoid `__new__` unless you must — and if you do, lock it and guard `__init__`.
- **TypeScript/Node**: an exported module instance is already a singleton; use a registry when you need named instances or test resets.
- **Anything testable**: skip the pattern entirely and inject the dependency — bind it as singleton in your DI container.

ES: [README.es.md](README.es.md)
