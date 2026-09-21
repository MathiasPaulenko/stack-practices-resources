# Iterator Pattern for Custom Collections — Companion Examples

Runnable TypeScript for the [Iterator pattern for custom collections](https://stackpractices.com/patterns/iterator-pattern-collections/): two traversal algorithms over one tree, an async paginated iterator, and a `LinkedList` that speaks `Symbol.iterator` so `for...of` works natively.

## What's inside

| File | Purpose |
| --- | --- |
| `iterators.ts` | `PreOrderIterator` (stack DFS), `LevelOrderIterator` (index-based BFS — O(1) per `next()`, no `queue.shift()`), `FileSystem` aggregate with a real path map, and `DatabaseQueryIterator` (async pagination). Prints both traversals and the paginated rows. |
| `linked-list.ts` | `LinkedList<T>` implementing `Iterable<T>` — `for...of`, spread, destructuring — plus generator-based `reverseIterator()` and `filterIterator()`. |
| `iterators.test.ts` | `node:test` suite (6 tests) covering pre-order, level-order, **post-order** traversal, exhaustion, `hasNext()` idempotency, and post-exhaustion `next()`. |

## Concepts covered

- **Traversal decoupled from structure** — the client's `while (it.hasNext())` never learns which algorithm ran.
- **O(1) breadth-first** — head index instead of `queue.shift()` (which reindexes every call, O(n²) total).
- **Async iteration** — `next(): Promise` hides `LIMIT/OFFSET` paging behind a uniform contract.
- **Symbol.iterator + generators** — native `for...of` ergonomics and lazy evaluation.

## Try it

```bash
npx ts-node iterators.ts
npx ts-node linked-list.ts
npx tsx --test iterators.test.ts
# or
deno run iterators.ts && deno run linked-list.ts
```
