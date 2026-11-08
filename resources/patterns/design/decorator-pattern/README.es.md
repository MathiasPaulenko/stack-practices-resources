# Patrón Decorator — Implementaciones ejecutables

Companion del patrón de StackPractices [Patrón Decorator](https://stackpractices.com/es/patterns/decorator-pattern/).

Demo de una pila de decoradores en tres implementaciones equivalentes: un componente `Coffee` envuelto por decoradores `Milk`, `Sugar` y `Whip`. Cada decorador añade su propio coste y etiqueta mientras delega el resto de la llamada al objeto envuelto. Solo stdlib — sin dependencias.

## Archivos

| Archivo | Stack | Ejecutar |
| --- | --- | --- |
| `src/decorator_stack.py` | Python 3.9+ (solo stdlib) | `python src/decorator_stack.py` |
| `src/decorator-stack.js` | Node.js 14+ (solo stdlib) | `node src/decorator-stack.js` |
| `src/DecoratorStack.java` | Java 11+ | `javac -d src src/DecoratorStack.java && java -cp src DecoratorStack` |

Cada ejecución imprime el componente simple, una pila completa (leche -> azúcar -> nata), los mismos decoradores en otro orden y una composición libre (doble leche) — mostrando que los decoradores se combinan en tiempo de ejecución en cualquier orden y que quien llama solo ve la interfaz `Coffee`.

El ejemplo usa el escenario clásico del café para mapear 1:1 con el artículo; la misma estructura alimenta los streams de I/O de Java, las funciones `@decorator` de Python y los pipelines de middleware HTTP.
