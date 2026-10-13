# Content Security Policy — Companion Files

Runnable CSP toolkit for the guide
[Content Security Policy: CSP Headers, Nonces, Hashes](https://stackpractices.com/guides/complete-guide-content-security-policy/):
per-request nonce middleware, a violation report endpoint, a helmet
config, and the Next.js middleware pattern.

## Files

| File | What it does |
| --- | --- |
| `app.ts` | Express demo app — wires the report endpoint, the `Reporting-Endpoints` header, and the nonce middleware; serves a page with one allowed and one blocked inline script. |
| `csp-nonce-middleware.ts` | Generates a `crypto.randomBytes` nonce per request, stores it in `res.locals.nonce`, and sets the enforcing CSP header. Includes the `Report-Only` variant for the discovery phase. |
| `csp-report-endpoint.ts` | POST `/api/csp-reports` — accepts both `application/reports+json` (Reporting API batches) and `application/csp-report` (legacy `report-uri`) payloads and normalizes them. |
| `helmet-csp.ts` | Equivalent policy expressed as a `helmet.contentSecurityPolicy` directives object, with nonce functions reading `res.locals.nonce`. |
| `nextjs-middleware.ts` | Next.js App Router `middleware.ts` — generates the nonce, sets the CSP header, forwards it via `x-nonce`. Reference snippet (requires a Next.js project). |
| `nextjs-layout.tsx` | `app/layout.tsx` — reads `x-nonce` with `headers()` and passes it to `<Script nonce>`. Reference snippet (requires a Next.js project). |

## Run

```bash
npm install
npm start        # demo app on http://localhost:3000
```

Open the page and check DevTools: the inline script carrying the nonce
executes, the one without it is blocked and reported. Post a violation
payload to `http://localhost:3000/api/csp-reports` to see the endpoint
accept both formats:

```bash
# Reporting API format (array of reports)
curl -X POST http://localhost:3000/api/csp-reports \
  -H "Content-Type: application/reports+json" \
  -d '[{"type":"csp-violation","body":{"document-uri":"http://localhost:3000/","blocked-uri":"inline","effective-directive":"script-src-elem"}}]'

# Legacy report-uri format
curl -X POST http://localhost:3000/api/csp-reports \
  -H "Content-Type: application/csp-report" \
  -d '{"csp-report":{"document-uri":"http://localhost:3000/","blocked-uri":"inline","violated-directive":"script-src"}}'
```

## Notes

- The nonce must be unpredictable (CSPRNG), unique per response, and the
  page must not be served as shared cached HTML.
- `'strict-dynamic'` lets nonced scripts load their own dependencies
  without maintaining a CDN allowlist; browsers without support fall
  back to the plain allowlist.
- The Next.js files are reference snippets — drop them into an App
  Router project; they are excluded from `tsconfig.json` because they
  need `next` as a dependency.
