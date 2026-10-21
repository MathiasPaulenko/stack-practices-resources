# Complete Guide to GraphQL Security

Hardened Apollo Server 4 setup matching the companion guide:
[Complete Guide to GraphQL Security](https://stackpractices.com/guides/complete-guide-graphql-security/) (ES: [Guía Completa de Seguridad en GraphQL](https://stackpractices.com/es/guides/complete-guide-graphql-security/)).

## Files

| File | What it covers |
| --- | --- |
| `server.js` | Full server wiring: Express + `expressMiddleware`, auth context, rate limit, body cap, timeouts, CORS |
| `introspection-gate.js` | Plugin that allows introspection only for admin users, inspecting the parsed operation AST |
| `auth-directive.js` | `@auth(requires: Role!)` schema directive via `mapSchema` + `getDirective` (graphql-tools v8+) |
| `cost-budget.js` | Redis-backed per-client cost budget for rate limiting by query cost |
| `package.json` | Dependency manifest with the versions used |

## Install

```bash
npm install
export NODE_ENV=production
node server.js
```

## What is enforced

- `introspection` off in production, gated by admin role elsewhere
- `hideSchemaDetailsFromClientErrors` to block field-suggestion enumeration
- `validationRules`: `graphql-depth-limit` + GraphQL Armor cost/alias/directive/token rules
- `allowBatchedHttpRequests` left at its `false` default + batch-size middleware
- `persistedQueries` with bounded TTL
- Per-IP `express-rate-limit` + per-identity cost budget in Redis
- `@auth` field-level authorization directive
- `formatError` masking (Apollo Server 4; move to plugin hooks on v5)

This is a starting point, not a drop-in — plug in your real schema, token verification, and Redis client.
