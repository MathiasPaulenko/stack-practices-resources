# Command Pattern (Undo/Redo) — Companion Resources

Companion code for the [Command pattern with undo/redo](https://stackpractices.com/patterns/command-pattern-undo/) on StackPractices.

## Files

| File | Language | Description |
| --- | --- | --- |
| `command_history.ts` | TypeScript (Node ≥ 22.18) | `CommandHistory` invoker with undo/redo stacks, `TextDocument` receiver, `InsertCommand`/`DeleteCommand`, `MacroCommand`, async `CommandQueue`, and bounded history |
| `test_command_history.ts` | TypeScript + `node:test` | 9 tests covering execute/undo/redo, redo-stack invalidation, macro reverse-order undo, history capping, and async serialization |

## Quick start

No dependencies — Node runs the `.ts` files directly via type stripping:

```bash
node command_history.ts          # demo: insert/undo/redo + macro
node --test test_command_history.ts
```

Expected: 9 passed tests and the demo output `Hello World / Hello / Hello World / ab`.
