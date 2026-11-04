# OAuth2/OIDC Production — Companion

Runnable TypeScript modules from the [Complete Guide to OAuth2 and OIDC in Production](https://stackpractices.com/guides/complete-guide-oauth2-oidc-production/).

## Files

- `pkce.ts` — PKCE verifier/challenge generation (RFC 7636)
- `env.ts` — fail-fast env var helper (throws at startup on missing config)
- `authorize.ts` — authorization URL builder (`response_type=code`, `S256`, `state`, `offline_access`)
- `callback.ts` — callback handler: constant-time `state` check + code exchange + session storage
- `jwt.ts` — JWKS-backed access-token validation + `authMiddleware` (jsonwebtoken + jwks-rsa)
- `oidc.ts` — async ID-token validation: signature, `aud`, `nonce`, required OIDC claims
- `refresh.ts` — refresh grant with rotation + auto-refresh middleware (60s buffer)
- `scopes.ts` — `requireScope` middleware returning RFC 6750 `insufficient_scope`
- `discovery.ts` — OIDC discovery document fetcher + typed config
- `clientCredentials.ts` — M2M client-credentials grant
- `revoke.ts` — token revocation call (RFC 7009)
- `introspect.ts` — token introspection for opaque tokens (RFC 7662)

## Usage

```bash
npm install
npx tsc
```

Set `OAUTH_CLIENT_ID`, `OAUTH_CLIENT_SECRET`, `M2M_CLIENT_ID`, `M2M_CLIENT_SECRET` and point `auth.example.com` at your IdP before wiring `callback.ts`, `jwt.ts`, `oidc.ts`, `refresh.ts` and `scopes.ts` into an Express app.

## Requirements

- Node.js 18+ (native `fetch`)
- `jsonwebtoken`, `jwks-rsa`, `express`, `express-session`
