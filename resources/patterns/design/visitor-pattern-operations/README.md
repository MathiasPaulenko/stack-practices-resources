# Visitor Pattern: Extensible Operations in TypeScript — Companion Code

Runnable versions of the visitor implementations from the
[Visitor Pattern: Extensible Operations in TypeScript](https://stackpractices.com/patterns/visitor-pattern-operations/)
resource on StackPractices.

## Files

| File | Description |
|------|-------------|
| `visitor-ast.ts` | Expression AST (`NumberNode`/`VariableNode`/`BinaryOpNode`) with `accept()` double dispatch and three visitors: `Evaluator`, `Printer`, `JSONSerializer` — each added without touching the node classes |
| `discriminated-union.ts` | The same AST and operations as a union type plus exhaustive `switch` — the lighter alternative compared in the resource |
| `visitor_ast.py` | Python port of the TS visitors for comparison |

## Requirements

- TypeScript — run with `npx tsx visitor-ast.ts` or `ts-node`
- Python 3.9+ — no dependencies, run `python visitor_ast.py`

## Notes

- Double dispatch is the point: `node.accept(visitor)` resolves the
  element type, then `visitor.visitX(this)` resolves the operation.
- `Evaluator` and `JSONSerializer` are stateful — the serializer must
  capture `this.result` between child traversals or left and right
  subtrees come out identical.
- `discriminated-union.ts` shows when Visitor is overkill: few pure
  operations, one small hierarchy. Same exhaustiveness guarantee from
  the compiler, a fraction of the code.
