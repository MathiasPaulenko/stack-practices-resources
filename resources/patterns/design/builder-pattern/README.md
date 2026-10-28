# Builder Pattern

Companion code for the pattern [Builder Pattern: Step-by-Step Object Construction](https://stackpractices.com/patterns/builder-pattern/).

## Contents

| File | What it is |
|------|------------|
| `pizza_builder.py` | Fluent `PizzaBuilder` with sensible defaults and validation inside `build()` |
| `query_builder.py` | Conditional SQL construction: `JOIN`, `WHERE`, `ORDER BY` and `LIMIT` applied only when needed |
| `pizza-builder.js` | JavaScript fluent builder plus a `toBuilder()` copy method for "same but different" variants |
| `Pizza.java` | Nested static `Builder` class, the Java convention, with a `main` demo |
| `database-config-builder.ts` | `DatabaseConfigBuilder` with environment presets (development / production) and secrets loaded from env vars |

## How to use

- Python: `python pizza_builder.py` and `python query_builder.py` — no dependencies beyond stdlib.
- JavaScript: `node pizza-builder.js`.
- TypeScript: `npx tsx database-config-builder.ts` or `npx ts-node database-config-builder.ts`.
- Java: `javac Pizza.java && java Pizza`.

Each file mirrors a section of the pattern page: basic fluent construction, validation in `build()`, copy methods, conditional construction, and configuration objects with environment presets.
