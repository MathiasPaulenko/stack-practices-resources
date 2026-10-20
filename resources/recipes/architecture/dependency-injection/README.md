# Dependency Injection — Companion Code

Runnable artifacts for the [Dependency Injection recipe](https://stackpractices.com/recipes/dependency-injection/) on StackPractices.

## Files

| File | What it is |
|------|------------|
| `di-container.ts` | ~60-line TypeScript container: transient / singleton / scoped lifecycles + `validate()` |
| `di_container.py` | Python container with scoped lifetime via context manager |
| `test-container.ts` | `TestContainer` that overrides production registrations with fakes, with vitest/jest usage |

## Usage

No dependencies. Copy the file you need into your project and adapt the registrations in the commented composition root. Call `validate()` at startup to fail fast on missing registrations, and scope per request/test.

## Related

- [Dependency Injection recipe (EN)](https://stackpractices.com/recipes/dependency-injection/)
- [Receta de Inyección de Dependencias (ES)](https://stackpractices.com/es/recipes/dependency-injection/)
- [StackPractices resources index](https://mathiaspaulenko.github.io/stack-practices-resources/)
