# Interpreter for Expression Languages — Companion Code

Companion code for the resource
[Interpreter Pattern for Domain-Specific Expression Languages](https://stackpractices.com/patterns/interpreter-pattern-expressions/).

A small rule engine where business rules ("20% off if cart > $100 AND user is VIP")
are composable expression trees evaluated against a context — stored as data,
not compiled into code.

## Files

| File | What it shows |
|------|---------------|
| `rule-engine.ts` | The full expression hierarchy (terminals + non-terminals), the two rule examples, and a recursive-descent formula parser that respects `*`/`/` precedence. Short-circuit `AND`/`OR` and a safe `DivideExpression` included. |
| `rules-factory.ts` | JSON rules → expression tree factory with a variable whitelist — the pattern for storing rules in a database and validating them at the boundary. |

## Run

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

Requires Node 20+ with `tsx` (`npx tsx` resolves it on the fly). No other dependencies.
