# Patrón Builder

Código companion del patrón [Patrón Builder: construcción de objetos paso a paso](https://stackpractices.com/es/patterns/builder-pattern/).

## Contenido

| Archivo | Qué es |
|---------|--------|
| `pizza_builder.py` | `PizzaBuilder` fluido con valores por defecto y validación dentro de `build()` |
| `query_builder.py` | Construcción SQL condicional: `JOIN`, `WHERE`, `ORDER BY` y `LIMIT` solo cuando hacen falta |
| `pizza-builder.js` | Builder fluido en JavaScript con un método de copia `toBuilder()` para variantes "igual pero distinta" |
| `Pizza.java` | Clase `Builder` estática anidada, la convención de Java, con demo en `main` |
| `database-config-builder.ts` | `DatabaseConfigBuilder` con presets por entorno (desarrollo / producción) y secretos cargados desde variables de entorno |

## Cómo usarlo

- Python: `python pizza_builder.py` y `python query_builder.py` — sin dependencias fuera de la stdlib.
- JavaScript: `node pizza-builder.js`.
- TypeScript: `npx tsx database-config-builder.ts` o `npx ts-node database-config-builder.ts`.
- Java: `javac Pizza.java && java Pizza`.

Cada archivo refleja una sección de la página del patrón: construcción fluida básica, validación en `build()`, métodos de copia, construcción condicional y objetos de configuración con presets por entorno.
