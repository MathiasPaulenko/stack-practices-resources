# Patrón Iterator — Ejemplos de Acompañamiento

Ejemplos ejecutables del [patrón Iterator](https://stackpractices.com/es/patterns/iterator-pattern/): la misma `BookCollection` construida sobre el protocolo de iteración nativo de cada lenguaje, más dos estrategias de recorrido sobre un mismo árbol binario tras un único contrato `Iterator`.

## Contenido

| Archivo | Propósito |
| --- | --- |
| `book_collection.py` | `BookCollection` con `__iter__` y un helper `reverse_iter()` — el protocolo de iterador de Python de punta a punta. |
| `book-collection.js` | `BookCollection` con `[Symbol.iterator]` y un generator `reverseIterator()` — `for...of` funciona de forma nativa. |
| `BookCollection.java` | `BookCollection implements Iterable<String>` más un `ReverseIterator<T>` hecho a mano — incluye `main` para ejecutar directo. |
| `tree-iterators.ts` | `InOrderIterator` (DFS con pila) y `BFSIterator` (cola) sobre `TreeNode<T>`, ambos tras la misma interfaz `Iterator` con `reset()` funcional. |
| `tree-iterators.test.ts` | Suite `node:test` que cubre ambos recorridos, agotamiento, idempotencia de `hasNext()` y `reset()`. |

## Conceptos cubiertos

- **Recorrido desacoplado de la estructura** — el `while (it.hasNext())` del cliente nunca descubre cómo se almacenan los elementos.
- **Protocolos nativos sobre interfaces propias** — `__iter__`, `Symbol.iterator` e `Iterable<T>` te regalan el patrón.
- **Varias posiciones simultáneas** — cada iterador guarda su propio estado, así que dos recorridos pueden correr en paralelo.
- **Fail-fast vs snapshot** — el intercambio que Java fija con `ConcurrentModificationException`.

## Pruébalo

```bash
python book_collection.py
node book-collection.js
javac BookCollection.java && java BookCollection
npx tsx tree-iterators.ts
npx tsx --test tree-iterators.test.ts
```
