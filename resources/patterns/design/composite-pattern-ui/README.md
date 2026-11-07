# Composite Pattern for UI Trees — Companion Resources

Runnable examples for the [Composite Pattern for UI Component Trees in React](https://stackpractices.com/patterns/composite-pattern-ui/) guide on StackPractices.

## Files

| File | What it shows |
|---|---|
| `ui-node.tsx` | The `UINode` discriminated union + recursive `<Node>` renderer for form trees |
| `form-tree.json` | The same tree as plain data — POST it, version it, render it |
| `nav-tree.tsx` | Second domain: a nested navigation menu rendered the same way |
| `serialization.test.mjs` | Round-trip + safety tests — run with `node serialization.test.mjs` |

## Notes

- Only composite members of the union carry `children` — the "safe" variant: leaves can't be given children by mistake.
- `serialization.test.mjs` verifies the two invariants the pattern promises: the tree survives `JSON.parse(JSON.stringify(t))` intact, and leaf nodes never carry a `children` field.
- To use `ui-node.tsx`/`nav-tree.tsx`, drop them into a React + TypeScript project; they're plain function components with no dependencies beyond React.

Source article (EN): <https://stackpractices.com/patterns/composite-pattern-ui/>
