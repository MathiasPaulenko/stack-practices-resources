# Patrón Memento (Snapshot de Estado) — Recursos Companion

Código companion del [patrón Memento para snapshots y restauración de estado](https://stackpractices.com/es/patterns/memento-pattern-state/) en StackPractices.

## Archivos

| Archivo | Lenguaje | Descripción |
| --- | --- | --- |
| `memento_history.ts` | TypeScript (Node ≥ 22.18) | Pila de undo `TextEditor`/`EditorSnapshot`/`EditorHistory`, `GameState`/`GameCheckpoint`, y wizard `FormEditor`/`FormMemento`/`FormHistory` con historial acotado |
| `test_memento_history.ts` | TypeScript + `node:test` | 8 tests que cubren undo/redo, invalidación de la rama redo, no-op en el snapshot más viejo, aislamiento del checkpoint con deep copy y restore del wizard |

## Inicio rápido

Sin dependencias — Node ejecuta los `.ts` directamente con type stripping:

```bash
node memento_history.ts          # demo: type/undo/redo + atrás en el wizard
node --test test_memento_history.ts
```

Esperado: 8 tests pasados y la salida de la demo `Hello World / Hello / Hello World / 1`.
