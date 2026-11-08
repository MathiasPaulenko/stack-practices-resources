# Dependency Injection Container — Runnable Implementations

Companion to the StackPractices pattern [Dependency Injection Container in TypeScript](https://stackpractices.com/patterns/dependency-injection-typescript/).

A minimal DI container in three languages: services register a factory under a token, and the container resolves the dependency graph lazily. Three lifetimes are demonstrated — singleton (one shared instance), transient (fresh per resolve), and scoped (one instance per request scope). Stdlib only, no dependencies.

## Files

| File | Stack | Run |
| --- | --- | --- |
| `src/di-container.js` | Node.js 18+ | `node src/di-container.js` |
| `src/di_container.py` | Python 3.10+ | `python src/di_container.py` |
| `src/DiContainer.java` | Java 11+ | `javac -d src src/DiContainer.java && java -cp src DiContainer` |

Each run wires the same graph — `UserService` → `UserRepository` → `Database` + `Logger` — and verifies the lifetime semantics: the singleton is shared across the root and every scope, transients are fresh objects, and each scope keeps its own copies.

The JavaScript file is a direct port of the article's TypeScript container (drop the types back in for production use). Python and Java show the same idea without decorators: the factory is the wiring, and injection happens only at the composition root.
