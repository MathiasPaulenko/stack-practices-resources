# Twin Pattern — Companion Code

Runnable versions of the Twin Pattern implementations from the
[Twin Pattern](https://stackpractices.com/patterns/twin-pattern/)
resource on StackPractices.

## Files

| File | Description |
|------|-------------|
| `twin_widget.py` | Python `Widget` + `Graphic`/`Interactive` twins with mutual references, a fail-fast check for unlinked twins, and a `unittest` suite covering delegation, stub-based twin isolation, and twin swapping |
| `twin-widget.ts` | TypeScript version with a `WidgetLike` interface so twins can be tested against stubs |

## Requirements

- Python 3.10+ (uses `typing.Protocol`; no external dependencies)
- TypeScript: `npx tsx twin-widget.ts` or compile with `tsc`

## Notes

- The back-reference is wired in the `Widget` constructor, so twins can
  never escape unlinked — the `linked()`/`_linked()` guards still throw a
  clear error if you build a twin by hand and forget `twin.widget = w`.
- `WidgetLike` is the minimal surface a twin reads (`name`, `x`, `y`,
  `width`, `height`). Injecting that interface instead of the concrete
  `Widget` is what makes twins unit-testable with a stub.
- In garbage-collected languages the Widget ↔ twin cycle is harmless. In
  C++/Rust use a weak back-reference (`weak_ptr`, `Rc<Weak>`).
