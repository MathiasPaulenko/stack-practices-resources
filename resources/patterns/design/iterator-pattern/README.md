# Iterator Pattern — Companion Examples

Runnable examples for the [Iterator pattern](https://stackpractices.com/patterns/iterator-pattern/): the same `BookCollection` built on each language's native iteration protocol, plus two traversal strategies over one binary tree that share a single `Iterator` contract.

## What's inside

| File | Purpose |
| --- | --- |
| `book_collection.py` | `BookCollection` with `__iter__` and a `reverse_iter()` helper — Python's iterator protocol end to end. |
| `book-collection.js` | `BookCollection` with `[Symbol.iterator]` and a `reverseIterator()` generator — `for...of` works natively. |
| `BookCollection.java` | `BookCollection implements Iterable<String>` plus a hand-rolled `ReverseIterator<T>` — includes `main` to run standalone. |
| `tree-iterators.ts` | `InOrderIterator` (stack DFS) and `BFSIterator` (queue) over `TreeNode<T>`, both behind the same `Iterator` interface with working `reset()`. |
| `tree-iterators.test.ts` | `node:test` suite covering both traversals, exhaustion, `hasNext()` idempotency, and `reset()`. |

## Concepts covered

- **Traversal decoupled from structure** — the client's `while (it.hasNext())` never learns how elements are stored.
- **Native protocols over custom interfaces** — `__iter__`, `Symbol.iterator` and `Iterable<T>` give you the pattern for free.
- **Multiple simultaneous positions** — each iterator tracks its own state, so two traversals can run side by side.
- **Fail-fast vs snapshot** — the trade-off Java bakes in with `ConcurrentModificationException`.

## Try it

```bash
python book_collection.py
node book-collection.js
javac BookCollection.java && java BookCollection
npx tsx tree-iterators.ts
npx tsx --test tree-iterators.test.ts
```
