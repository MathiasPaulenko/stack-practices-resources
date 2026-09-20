# Prototype Pattern — Companion Resources

Runnable examples for the [Prototype pattern](https://stackpractices.com/patterns/prototype-pattern/) on StackPractices.

The pattern stamps out new objects by copying a configured instance instead of rebuilding from scratch. Both implementations ship a `PrototypeRegistry`: a map of named prototypes that returns an independent clone on every `get()`.

## Files

| File | What it shows |
|------|---------------|
| `prototype.py` | `ProductConfig` prototype + `PrototypeRegistry` in Python — `copy.deepcopy` for nested-structure independence |
| `test_prototype.py` | pytest suite: 6 tests covering clone identity, deep-copy independence, registry isolation, unknown keys, non-clonable rejection |
| `prototype.js` | The same registry in JavaScript — a *manual* `clone()` that preserves the class (and a comment on why `structuredClone` doesn't) |
| `prototype.test.js` | `node:test` suite: 7 tests including the `instanceof` preservation case |

## Run it

```bash
# Python demo + tests
python prototype.py
python -m pytest test_prototype.py -v

# JavaScript demo + tests (Node 18+)
node prototype.js
node --test prototype.test.js
```

## Key takeaways

- Deep copy is what makes clones independent — nested `attributes`/`tags` are duplicated so mutating a clone never touches the prototype.
- `structuredClone` copies the data but drops the prototype chain; the JS example clones manually to keep `instanceof` and methods working.
- Registered prototypes are treated as read-only: callers always work on clones.
- Cloning beats construction only when initialization is expensive (parsing, I/O, graph wiring) — for plain field assignment, a constructor is faster.

CI: `.github/workflows/test.yml` runs both test suites on every change to this folder.
