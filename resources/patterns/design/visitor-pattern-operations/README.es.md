# Patrón Visitor: Operaciones Extensibles en TypeScript — Código complementario

Versiones ejecutables de las implementaciones visitor del recurso
[Patrón Visitor: Operaciones Extensibles en TypeScript](https://stackpractices.com/es/patterns/visitor-pattern-operations/)
de StackPractices.

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `visitor-ast.ts` | AST de expresiones (`NumberNode`/`VariableNode`/`BinaryOpNode`) con double dispatch vía `accept()` y tres visitors: `Evaluator`, `Printer`, `JSONSerializer` — cada uno añadido sin tocar las clases de nodo |
| `discriminated-union.ts` | El mismo AST y operaciones como tipo unión más `switch` exhaustivo — la alternativa ligera comparada en el recurso |
| `visitor_ast.py` | Port a Python de los visitors en TS para comparación |

## Requisitos

- TypeScript — ejecuta con `npx tsx visitor-ast.ts` o `ts-node`
- Python 3.9+ — sin dependencias, ejecuta `python visitor_ast.py`

## Notas

- El double dispatch es el punto: `node.accept(visitor)` resuelve el
  tipo de elemento, luego `visitor.visitX(this)` resuelve la operación.
- `Evaluator` y `JSONSerializer` mantienen estado — el serializador debe
  capturar `this.result` entre recorridos de hijos o los subárboles
  izquierdo y derecho salen idénticos.
- `discriminated-union.ts` muestra cuándo Visitor es exceso: pocas
  operaciones puras, una jerarquía pequeña. Misma garantía de
  exhaustividad del compilador con una fracción del código.
