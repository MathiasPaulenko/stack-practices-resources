# Mixin Pattern — Companion Code

Runnable versions of the Mixin Pattern implementations from the
[Mixin Pattern](https://stackpractices.com/patterns/mixin-pattern/)
resource on StackPractices.

## Files

| File | Description |
|------|-------------|
| `mixins.py` | Python `SerializableMixin` + `TimestampMixin` composed into `User` through cooperative multiple inheritance, plus a `unittest` suite that tests the mixin against a throwaway host class and documents the MRO |
| `mixins.ts` | TypeScript typed mixins (`Loggable`, `Serializable`, `Validatable`) as functions that wrap a base class — `EnhancedUser` keeps every mixed-in method fully typed |

## Requirements

- Python 3.10+ (stdlib only)
- TypeScript: `npx tsx mixins.ts` or compile with `tsc`

## Notes

- The cooperative `super().__init__(*args, **kwargs)` in each Python mixin is what keeps the MRO chain alive. Remove it and every class to the right of it in `class User(TimestampMixin, SerializableMixin)` silently never initializes.
- `User.__mro__` is `User → TimestampMixin → SerializableMixin → object`, so the leftmost mixin wins any name conflict. Order is semantics, not style.
- In TypeScript the mixin order works the same way at the type level: `Loggable(Serializable(Validatable(User)))` produces a different composed class than any other permutation.
- For JavaScript `Object.assign`-style mixins remember that getters are evaluated once at copy time — use `Object.getOwnPropertyDescriptors` + `Object.defineProperties` to preserve them.
