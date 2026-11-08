# Data Validation with Zod — Companion Examples

Runnable examples for the recipe [Schema-Based Data Validation with Zod in TypeScript](https://stackpractices.com/recipes/data-validation-zod/). All schemas target **Zod 4** top-level APIs (`z.uuid()`, `z.email()`, `z.url()`).

## Files

| File | What it shows |
|------|---------------|
| `schemas/user.ts` | Basic object schema, `z.infer`, custom `.refine` password rules |
| `schemas/env.ts` | Fail-fast `process.env` validation at startup with `z.coerce` |
| `schemas/webhook.ts` | `z.discriminatedUnion` for polymorphic webhook payloads |
| `middleware/validate-body.ts` | Express middleware + `error.issues` → `{ field: message }` formatter |

## Run

```bash
npm install zod
node --experimental-strip-types schemas/user.ts
```

`env.ts` and `webhook.ts` are meant to be dropped into a project — `env.ts` exits the process on invalid config, and `validate-body.ts` needs `express` types.
