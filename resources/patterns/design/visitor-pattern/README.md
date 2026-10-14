# Visitor Pattern — Companion Code

Runnable versions of the visitor implementations from the
[Visitor Pattern](https://stackpractices.com/patterns/visitor-pattern/)
resource on StackPractices.

## Files

| File | Description |
|------|-------------|
| `visitor_pattern.py` | Expression AST (`Number`/`Add`/`Mul`) with `accept()` double dispatch and three visitors: `EvalVisitor`, `PrintVisitor`, `CountNodesVisitor` — the last one added without touching any `Expr` class |
| `visitor-pattern.ts` | Same AST in TypeScript with a generic `ExprVisitor<R>` interface — the visitor return type is part of the contract |

## Requirements

- Python 3.9+ — no dependencies, run `python visitor_pattern.py`
- TypeScript — run with `npx tsx visitor-pattern.ts` or `ts-node`

## Notes

- Double dispatch is the point: `expr.accept(visitor)` resolves the
  element type, then `visitor.visitX(this)` resolves the operation.
- Adding a new *operation* is free (a new visitor). Adding a new *element
  type* is expensive — every visitor needs a new `visitX`, which the
  compiler enforces in the TypeScript version.
- Visitors that accumulate results (like `EvalVisitor`'s recursion) keep
  no shared mutable state here — safe to reuse across traversals.
