# Marker Interface Pattern — Companion Resources

Companion code for [Marker Interface Pattern](https://stackpractices.com/patterns/marker-interface-pattern/).

Runnable demos of the pattern in three languages, each showing the same idea — an empty type tag plus a runtime check — implemented with each language's own mechanism.

## Contents

| File | What it shows |
| --- | --- |
| `marker_demo.py` | Empty `ABC` base classes as markers + `isinstance` checks. Includes the proof that the check discriminates (`User` vs `SerializableUser`). Note: an empty `Protocol` would match everything — see the module docstring. |
| `MarkerDemo.java` | Custom marker interfaces (`Auditable`, `Immutable`) with `instanceof` checks. Compile and run standalone: `javac MarkerDemo.java && java MarkerDemo`. |
| `marker-demo.js` | `Symbol` keys as markers on class constructors + static checks. Run: `node marker-demo.js`. |

## How to use

1. Run each demo and confirm the marked class passes and the unmarked one is rejected.
2. Try marking `SecretData`/`MutableConfig` and watch the checks flip.
3. Compare mechanisms: base class (Python), interface (Java), symbol (JS) — same pattern, different runtime machinery.
