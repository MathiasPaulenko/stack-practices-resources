# Test Strategy Document Template — Companion Resources

Downloadable files for the [Test Strategy Document Template](https://stackpractices.com/docs/test-strategy-document-template/) article.

## Files

| File | Purpose |
|------|---------|
| `test-strategy-template.md` | Blank 12-section test strategy template: objectives, pyramid, scope, environments, tools, CI gates, data, flaky policy, metrics, risks, roles, review cycle |
| `test-strategy-payments-example.md` | Filled example for a payments microservice: stricter coverage gates, contract tests slice, Stripe-specific risks |

## How to use

1. Copy `test-strategy-template.md` into your repo as `TEST_STRATEGY.md`.
2. Fill the scope table first — it forces the coverage-priority conversation with your tech lead and PM.
3. Adjust the pyramid percentages to your domain and record why in the rationale.
4. Wire the coverage gates into CI before publishing the document.
5. Use `test-strategy-payments-example.md` as a reference for how a critical service deviates from the defaults.

Spanish version: [Plantilla de Estrategia de Pruebas](https://stackpractices.com/es/docs/test-strategy-document-template/)
