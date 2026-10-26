# Abstract Factory Pattern

Companion code for the pattern [Abstract Factory Pattern](https://stackpractices.com/patterns/abstract-factory-pattern/).

## Contents

| File | What it is |
|------|------------|
| `abstract_factory.py` | Product families (`Light`/`Dark` Button+Checkbox) plus a `FactoryRegistry` for runtime family selection |
| `ui_factory.js` | JavaScript interfaces, a `LightUIFactory`, and a `LazyUIFactory` proxy deferring instantiation to first use |
| `UIFactory.java` | Java interfaces, `LightUIFactory`, and `FactoryLoader` for config-driven loading via reflection |

## How to use

- Python: `python abstract_factory.py` — no dependencies beyond stdlib.
- JavaScript: `node ui_factory.js`.
- Java: compile and wire via `FactoryLoader.loadFactory("LightUIFactory")` or instantiate directly.

Each file mirrors a section of the pattern page: base implementation, registry-based selection, lazy proxy, and reflection loading.
