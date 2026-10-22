# Clean Code Principles — Before & After Companion

Companion exercise for the guide [Clean Code Principles: Naming, Functions, Classes](https://stackpractices.com/guides/complete-guide-clean-code-principles/).

## Files

| File | What it shows |
|------|---------------|
| `before/order-manager.ts` | A deliberately messy `OrderManager`: 30-line function, magic numbers, error codes, hidden mutation, unpronounceable names |
| `after/order-processor.ts` | The same logic refactored: small functions, SRP collaborators, named constants, exceptions, no side effects |
| `eslint.config.mjs` | ESLint rules that enforce the principles mechanically (`max-params`, `complexity`, `no-magic-numbers`, `max-depth`) |

## Exercise

1. Read `before/order-manager.ts` and list every smell you can find (aim for at least 8).
2. Refactor it yourself before opening `after/`.
3. Compare your version with `after/order-processor.ts` — the differences are discussion points, not a score.
4. Run the lint config against `before/` to see which smells a tool can catch automatically:

```bash
npm install eslint
npx eslint before/ --config eslint.config.mjs
```

Tools catch the mechanical smells (size, depth, magic numbers). The semantic ones — a name that lies, a side effect that surprises — still need a human review.
