# Patrón Iterator para Colecciones Personalizadas — Ejemplos de Acompañamiento

TypeScript ejecutable del [patrón Iterator para colecciones personalizadas](https://stackpractices.com/es/patterns/iterator-pattern-collections/): dos algoritmos de recorrido sobre un mismo árbol, un iterador paginado asíncrono, y una `LinkedList` que habla `Symbol.iterator` para que `for...of` funcione de forma nativa.

## Contenido

| Archivo | Propósito |
| --- | --- |
| `iterators.ts` | `PreOrderIterator` (DFS con pila), `LevelOrderIterator` (BFS con índice — O(1) por `next()`, sin `queue.shift()`), agregado `FileSystem` con mapa de rutas real, y `DatabaseQueryIterator` (paginación asíncrona). Imprime ambos recorridos y las filas paginadas. |
| `linked-list.ts` | `LinkedList<T>` implementando `Iterable<T>` — `for...of`, spread, destructuring — más `reverseIterator()` y `filterIterator()` basados en generators. |
| `iterators.test.ts` | Suite `node:test` (6 tests) que cubre recorrido pre-order, level-order, **post-order**, agotamiento, idempotencia de `hasNext()` y `next()` tras agotarse. |

## Conceptos cubiertos

- **Recorrido desacoplado de la estructura** — el `while (it.hasNext())` del cliente nunca descubre qué algoritmo se ejecutó.
- **Anchura en O(1)** — índice `head` en lugar de `queue.shift()` (que reindexa en cada llamada, O(n²) total).
- **Iteración asíncrona** — `next(): Promise` oculta la paginación `LIMIT/OFFSET` tras un contrato uniforme.
- **Symbol.iterator + generators** — ergonomía nativa de `for...of` y evaluación perezosa.

## Pruébalo

```bash
npx ts-node iterators.ts
npx ts-node linked-list.ts
npx tsx --test iterators.test.ts
# o
deno run iterators.ts && deno run linked-list.ts
```
