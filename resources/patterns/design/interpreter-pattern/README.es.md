# Patrón Interpreter — Código complementario

Implementaciones ejecutables que acompañan a [Patrón Interpreter](https://stackpractices.com/es/patterns/interpreter-pattern/) en StackPractices.

## Archivos

| Archivo | Lenguaje | Qué muestra |
|---------|----------|-------------|
| `interpreter_pattern.py` | Python | AST de expresiones aritméticas (`Number`, `Variable`, `Add`, `Subtract`) evaluado contra un dict de contexto |
| `interpreter-pattern.js` | JavaScript | El mismo lenguaje aritmético con clases y defaults `??` |
| `InterpreterPattern.java` | Java | El mismo lenguaje aritmético como una única clase compilable |
| `config-dsl.ts` | TypeScript | Un mini DSL de comandos (`SET`/`GET`/`DEL`) con un parser artesanal que produce un `SequenceExpression` |

## Ejecutar

```bash
python interpreter_pattern.py        # 8
node interpreter-pattern.js          # 8
javac InterpreterPattern.java && java InterpreterPattern   # 8.0
npx ts-node config-dsl.ts            # líneas OK/OK/Alice/OK
```

Cada ejemplo construye el AST (con parser en `config-dsl.ts`, a mano en los aritméticos) y llama a `interpret()` en la raíz contra un contexto con las variables.
