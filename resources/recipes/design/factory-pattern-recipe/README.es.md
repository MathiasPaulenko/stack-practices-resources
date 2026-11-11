# Receta Patrón Factory — Recursos complementarios

Ejemplos de código de la receta [Crea Objetos de Forma Flexible con el Patrón Factory](https://stackpractices.com/es/recipes/factory-pattern-recipe/).

## Archivos

| Archivo | Qué muestra |
|---------|-------------|
| `notification-factory.ts` | Factory Method: las subclases de `NotificationFactory` eligen `EmailNotifier`/`SmsNotifier` en runtime (TypeScript) |
| `payment-factory.py` | Simple Factory: `PaymentProcessorFactory.create("stripe")` devuelve el `PaymentProcessor` correcto, config por variables de entorno (Python — ejecutable) |
| `UIFactoryDemo.java` | Abstract Factory: `WindowsUIFactory`/`MacUIFactory` producen familias coherentes de widgets (Java — `javac` + `java`) |
| `di-container.ts` | Contenedor DI mínimo con factory providers `bind`/`resolve` y caché singleton (TypeScript) |
| `notification-builder.ts` | Combo Factory + Builder: el builder elige canal y envuelve el producto en un `ResilientNotifier` con reintentos (TypeScript) |
| `async-db-factory.py` | Factory async con pool `asyncpg` perezoso protegido por lock (Python — necesita PostgreSQL) |

## Notas

- `payment-factory.py` y `UIFactoryDemo.java` corren solos. Los TypeScript asumen `tsx`/top-level await ESM; `async-db-factory.py` necesita `pip install asyncpg` y PostgreSQL.
- Los secretos vienen de variables de entorno con fallbacks de desarrollo — nunca incrustes credenciales en las factories.
