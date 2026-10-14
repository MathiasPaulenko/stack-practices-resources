# Dependency Injection Pattern — Companion Code

Runnable examples accompanying the
[Dependency Injection Pattern](https://stackpractices.com/patterns/dependency-injection-pattern/)
resource on StackPractices.

## Files

| File | Description |
|------|-------------|
| `dependency_injection.py` | `OrderService` receiving `PaymentProcessor` + `Logger` via constructor — manual wiring in `composition_root()` plus a minimal `Container` with singleton scope |
| `dependency-injection.ts` | Same shape in TypeScript — typed `Container` using abstract classes as injection tokens |

## Requirements

- Python 3.9+ — no dependencies, run `python dependency_injection.py`
- TypeScript — run with `npx tsx dependency-injection.ts` or `ts-node`

## Notes

- The container is a teaching tool (~30 lines): real projects should use
  tsyringe, InversifyJS, Spring, or whatever their framework provides.
- Watch the failure mode: `resolve()` on an unregistered token throws —
  that's the runtime wiring error DI trades for flexibility.
- Singleton registration shows where per-request state bugs come from:
  a `Logger` singleton is fine, a request-scoped dependency is not.
