# Aggregate Pattern — Companion

Runnable examples of the Aggregate pattern from [StackPractices](https://stackpractices.com/patterns/aggregate-pattern/).

The `Order` class acts as an aggregate root. It guards the invariant that a submitted order must have at least one line, and it prevents modifications after submission.

## Files

- `src/aggregate_pattern.py` — Python dataclass version
- `src/aggregate-pattern.js` — JavaScript class version
- `src/Aggregate.java` — Java `record` version

## Run

```bash
python src/aggregate_pattern.py
node src/aggregate-pattern.js
javac src/Aggregate.java && java -cp src Order
```
