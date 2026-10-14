# Patrón Visitor — Código complementario

Versiones ejecutables de las implementaciones de visitor del recurso
[Patrón Visitor](https://stackpractices.com/es/patterns/visitor-pattern/)
en StackPractices.

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `visitor_pattern.py` | AST de expresiones (`Number`/`Add`/`Mul`) con doble despacho `accept()` y tres visitors: `EvalVisitor`, `PrintVisitor`, `CountNodesVisitor` — el último añadido sin tocar ninguna clase `Expr` |
| `visitor-pattern.ts` | El mismo AST en TypeScript con interfaz genérica `ExprVisitor<R>` — el tipo de retorno del visitor forma parte del contrato |

## Requisitos

- Python 3.9+ — sin dependencias, corre con `python visitor_pattern.py`
- TypeScript — corre con `npx tsx visitor-pattern.ts` o `ts-node`

## Notas

- El doble despacho es la clave: `expr.accept(visitor)` resuelve el tipo
  de elemento y luego `visitor.visitX(this)` resuelve la operación.
- Añadir una *operación* nueva es gratis (un visitor nuevo). Añadir un
  *tipo de elemento* nuevo es caro — cada visitor necesita un `visitX`
  nuevo, y el compilador lo exige en la versión TypeScript.
- Los visitors que acumulan resultados (como la recursión de
  `EvalVisitor`) no guardan estado mutable compartido — se pueden
  reutilizar entre recorridos sin problema.
