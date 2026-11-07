# Composite Pattern — Companion Resources

Runnable examples for the [Composite Pattern](https://stackpractices.com/patterns/composite-pattern/) guide on StackPractices.

## Files

| File | What it shows |
|---|---|
| `file_system.py` | File/Folder composite tree in Python — run with `python file_system.py` |
| `file-system.js` | Same example in JavaScript — run with `node file-system.js` |
| `FileSystem.java` | Same example in Java — `javac FileSystem.java && java FileSystem` |
| `expression-tree.ts` | Second domain: arithmetic expression tree with `eval()` — `npx tsx expression-tree.ts` |
| `test_cycle_check.py` | Safe `add()` that rejects cycles + unittest suite — `python test_cycle_check.py` |

## Notes

- The file-system examples use the **safe** variant: `add()`/`remove()` exist only on `Folder`, not on the shared interface.
- `test_cycle_check.py` demonstrates the ancestor check described in the FAQ — inserting a folder into its own subtree raises `ValueError`.
- The expression tree shows why the pattern generalizes beyond containers: operators and numbers share `eval()`.

Source article (EN): <https://stackpractices.com/patterns/composite-pattern/>
