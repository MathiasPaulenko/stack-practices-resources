# Circuit Breaker Pattern Recipe Resources

Companion for [Build Resilient Systems with the Circuit Breaker Pattern](https://stackpractices.com/recipes/circuit-breaker-pattern-recipe/).

## Files

| File | Description |
|------|-------------|
| `impl/` | Copy-paste circuit breaker implementations extracted from the recipe (multiple languages) |

## Usage

Drop the implementation for your stack into your project; wrap outbound calls with `.call(fn)` / `await breaker.execute(fn)` depending on the language. Tune `failureThreshold`, `resetTimeout`, and the fallback to your service.
