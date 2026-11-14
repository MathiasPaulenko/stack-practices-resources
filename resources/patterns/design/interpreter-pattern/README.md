# Interpreter Pattern — Companion Code

Runnable implementations accompanying [Interpreter Pattern](https://stackpractices.com/patterns/interpreter-pattern/) on StackPractices.

## Files

| File | Language | What it shows |
|------|----------|---------------|
| `interpreter_pattern.py` | Python | Arithmetic expression AST (`Number`, `Variable`, `Add`, `Subtract`) evaluated against a context dict |
| `interpreter-pattern.js` | JavaScript | Same arithmetic language with classes and `??` defaults |
| `InterpreterPattern.java` | Java | Same arithmetic language as a single compilable class |
| `config-dsl.ts` | TypeScript | A small command DSL (`SET`/`GET`/`DEL`) with a hand-rolled parser producing a `SequenceExpression` |

## Run

```bash
python interpreter_pattern.py        # 8
node interpreter-pattern.js          # 8
javac InterpreterPattern.java && java InterpreterPattern   # 8.0
npx ts-node config-dsl.ts            # OK/OK/Alice/OK lines
```

Each example builds the AST (parser-fed in `config-dsl.ts`, hand-built in the arithmetic ones) and calls `interpret()` on the root against a context holding variable bindings.
