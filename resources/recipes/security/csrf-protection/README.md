# CSRF Protection — Companion Examples

Runnable companion for the recipe [CSRF Protection: How to Secure Web Forms](https://stackpractices.com/recipes/csrf-protection/).

## Contents

- `csrf-middleware.js` — Express middleware implementing the **signed double-submit cookie** pattern: issues an HMAC-signed token cookie and verifies the `X-CSRF-Token` header on every mutating request, with constant-time comparison.
- `demo-server.js` — minimal Express server wiring the middleware plus a test form that reads the cookie and echoes the token in the header.

## Run

```bash
npm install express cookie-parser
CSRF_SECRET=dev-secret node demo-server.js
# open http://localhost:3000
```

Submitting the form sends `POST /api/transfer` with the token header — a 200. Replay the same POST without the header (e.g., from curl or a cross-site page) and you get a 403.

## What it demonstrates

- Token issuance with HMAC signature (stateless — nothing stored server-side).
- `SameSite=Strict` + `Secure` on the token cookie.
- Length-guarded `crypto.timingSafeEqual` so forged cookies get 403, not 500.
- Why a custom header defeats cross-site forgery: browsers never set `X-CSRF-Token` on credentialed cross-site requests.
