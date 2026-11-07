# Complete Guide to Web Security Headers — Examples

Runnable companion for the StackPractices guide
[Complete Guide to Web Security Headers](https://stackpractices.com/guides/complete-guide-web-security-headers/).

Self-contained Express + Helmet project that matches the guide's server configuration and proves it with tests:

- `src/app.js` — helmet with the guide's CSP directives (`default-src 'self'`, `frame-ancestors 'none'`, `object-src 'none'`), HSTS with `includeSubDomains` + `preload`, `X-Frame-Options: DENY`, `strict-origin-when-cross-origin` referrer policy, and COOP/CORP. Both violation report endpoints are included: legacy `report-uri` (`application/csp-report`) and the modern Reporting API (`application/reports+json`).
- `src/server.js` — listens on `PORT` or `3000`.
- `tests/headers.test.js` — supertest assertions that every header lands on responses, the CSP contains the expected directives and never `unsafe-inline`/`unsafe-eval`, API responses carry the same policy, and both report endpoints return 204.

## Run

```bash
npm install
npm start          # serves on http://localhost:3000
npx vitest run     # verifies all headers and report endpoints
```

Requires Node 20+. `.github/workflows/test.yml` runs the same suite in CI.
