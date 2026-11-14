# Interpreter para Lenguajes de Expresión — Código complementario

Código complementario del recurso
[Patrón Interpreter para Lenguajes de Expresión](https://stackpractices.com/es/patterns/interpreter-pattern-expressions/).

Un pequeño motor de reglas donde las reglas de negocio ("20% de descuento si el
carrito > $100 Y el usuario es VIP") son árboles de expresiones componibles que
se evalúan contra un contexto — almacenadas como datos, no compiladas en código.

## Archivos

| Archivo | Qué muestra |
|---------|-------------|
| `rule-engine.ts` | La jerarquía completa de expresiones (terminales + no terminales), los dos ejemplos de reglas y un parser de fórmulas por descenso recursivo que respeta la precedencia de `*`/`/`. Incluye `AND`/`OR` con short-circuit y una `DivideExpression` segura. |
| `rules-factory.ts` | Factory de reglas JSON → árbol de expresiones con whitelist de variables — el patrón para almacenar reglas en una base de datos y validarlas en la frontera. |

## Ejecutar

```bash
npx tsx rule-engine.ts
# cart>100 AND isVIP: true
# access: false
# price * 0.8 + shipping: 90
# 1 + 2 * 3: 7

npx tsx rules-factory.ts
# discount rule: true
# discount rule (not vip): false
# blocked: unknown variable: "process.env"
```

Requiere Node 20+ con `tsx` (`npx tsx` lo resuelve al vuelo). Sin otras dependencias.
