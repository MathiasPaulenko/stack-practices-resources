# Entity-Component-System (ECS) Pattern — Companion Resources

Runnable minimal ECS implementations in Python, Java and JavaScript. Each file is self-contained and prints a small demo when executed.

**Article**: https://stackpractices.com/patterns/entity-component-system-pattern/

## Files

| File | Language | Run |
|------|----------|-----|
| `ecs_world.py` | Python 3.10+ | `python ecs_world.py` |
| `EcsWorld.java` | Java 11+ | `javac EcsWorld.java && java Demo` |
| `ecs-world.js` | Node.js 18+ | `node ecs-world.js` |
| `README.md` / `README.es.md` | — | This file, in English and Spanish |

## What it shows

- Entities as bare IDs (`uuid`/`UUID`/`crypto.randomUUID`)
- Pure-data components (`@dataclass`, plain classes, plain JS objects)
- `World.query(...)` as set intersection over component types
- Systems iterating only the entities that match their query
- Runtime component attachment — grant `FlyingComponent` to a live entity without creating a new class

## Source

Part of the StackPractices companion resources. The article explains variants (sparse set, archetype, chunk-based, event-driven), when the pattern pays off and when it doesn't.
