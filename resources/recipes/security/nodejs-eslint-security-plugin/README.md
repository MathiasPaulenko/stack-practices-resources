# ESLint Security Plugin — Companion

Companion code for the recipe [Enforce Security Rules in Node.js with ESLint](https://stackpractices.com/recipes/nodejs-eslint-security-plugin/).

## What's inside

- `eslint.config.js` — flat-config setup with `eslint-plugin-security` tuned per severity (`error` for eval/child_process/ReDoS, `warn` for non-literal paths, `off` for `detect-object-injection`), plus a relaxed override for `test/`.
- `vulnerable.js` — a deliberately insecure HTTP server so the plugin has something real to flag (path traversal, ReDoS, eval, deprecated `Buffer`, weak randomness, shell injection).
- `fixed.js` — the same endpoints rewritten to produce zero findings.
- `eslint-security.yml` — GitHub Actions gate that runs the linter and fails the build on any new `security/*` error.
- `package.json` — minimal dev dependencies and lint scripts.

## Try it

```bash
npm install
npx eslint vulnerable.js   # ~6 security findings
npx eslint fixed.js        # clean
```

Drop `eslint-security.yml` into `.github/workflows/` to enforce the gate in CI.

ES version: [README.es.md](./README.es.md)
