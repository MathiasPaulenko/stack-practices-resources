# Null Object Pattern — Companion Code

Runnable examples from [Null Object Pattern](https://stackpractices.com/patterns/null-object-pattern/) on StackPractices.

A null object implements the same interface as the real one but returns safe defaults — `"Guest"`, `false`, empty lists, no-ops — so callers never branch on `null`.

## Files

- `null_user.py` — `User` ABC + `RealUser` + `NullUser` with a `find_user()` lookup that never returns `None`. Run: `python null_user.py`
- `null_logger.js` — `OrderService` with `Logger`/`AppConfig` collaborators injected through the constructor; `NullLogger`/`NullConfig` give silent test runs without a mocking framework. Run: `node null_logger.js`
- `NullUser.java` — same `User` interface in Java with a `Demo` main. Run: `javac NullUser.java && java NullUser\$Demo`

## Key idea

`findUser(999)` returns a `NullUser`, not `null` — `user.getName()` works without a guard clause. The "user not found" branch lives inside the object graph instead of every call site.
