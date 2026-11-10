# Patrón Entity-Component-System (ECS) — Recursos complementarios

Implementaciones ECS mínimas ejecutables en Python, Java y JavaScript. Cada archivo es autocontenido e imprime una pequeña demo al ejecutarse.

**Artículo**: https://stackpractices.com/es/patterns/entity-component-system-pattern/

## Archivos

| Archivo | Lenguaje | Ejecutar |
|---------|----------|----------|
| `ecs_world.py` | Python 3.10+ | `python ecs_world.py` |
| `EcsWorld.java` | Java 11+ | `javac EcsWorld.java && java Demo` |
| `ecs-world.js` | Node.js 18+ | `node ecs-world.js` |
| `README.md` / `README.es.md` | — | Este archivo, en inglés y español |

## Qué muestra

- Entidades como IDs desnudos (`uuid`/`UUID`/`crypto.randomUUID`)
- Componentes de datos puros (`@dataclass`, clases simples, objetos JS planos)
- `World.query(...)` como intersección de conjuntos sobre tipos de componente
- Sistemas que iteran solo sobre las entidades que cumplen su query
- Adjuntar componentes en runtime — concede `FlyingComponent` a una entidad viva sin crear una clase nueva

## Fuente

Parte de los recursos complementarios de StackPractices. El artículo explica las variantes (sparse set, archetype, chunk-based, event-driven), cuándo compensa el patrón y cuándo no.
