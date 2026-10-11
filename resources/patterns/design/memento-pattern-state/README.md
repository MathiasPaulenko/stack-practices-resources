# Memento Pattern (State Snapshot) — Companion Resources

Companion code for the [Memento pattern for state snapshot and restoration](https://stackpractices.com/patterns/memento-pattern-state/) on StackPractices.

## Files

| File | Language | Description |
| --- | --- | --- |
| `memento_history.ts` | TypeScript (Node ≥ 22.18) | `TextEditor`/`EditorSnapshot`/`EditorHistory` undo stack, `GameState`/`GameCheckpoint`, and `FormEditor`/`FormMemento`/`FormHistory` wizard with bounded history |
| `test_memento_history.ts` | TypeScript + `node:test` | 8 tests covering undo/redo, redo-branch invalidation, no-op at the oldest snapshot, checkpoint deep-copy isolation, and wizard restore |

## Quick start

No dependencies — Node runs the `.ts` files directly via type stripping:

```bash
node memento_history.ts          # demo: type/undo/redo + wizard back
node --test test_memento_history.ts
```

Expected: 8 passed tests and the demo output `Hello World / Hello / Hello World / 1`.
