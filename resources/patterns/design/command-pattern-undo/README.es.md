# Patrón Command (Undo/Redo) — Recursos companion

Código companion del [patrón Command con undo/redo](https://stackpractices.com/es/patterns/command-pattern-undo/) en StackPractices.

## Archivos

| Archivo | Lenguaje | Descripción |
| --- | --- | --- |
| `command_history.ts` | TypeScript (Node ≥ 22.18) | Invoker `CommandHistory` con pilas undo/redo, receiver `TextDocument`, `InsertCommand`/`DeleteCommand`, `MacroCommand`, `CommandQueue` async e historial acotado |
| `test_command_history.ts` | TypeScript + `node:test` | 9 tests: execute/undo/redo, invalidación de la pila redo, undo de macro en orden inverso, historial acotado y serialización async |

## Inicio rápido

Sin dependencias — Node ejecuta los `.ts` directo con type stripping:

```bash
node command_history.ts          # demo: insert/undo/redo + macro
node --test test_command_history.ts
```

Esperado: 9 tests en verde y la salida del demo `Hello World / Hello / Hello World / ab`.
