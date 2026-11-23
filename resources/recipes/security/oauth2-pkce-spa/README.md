# OAuth 2.0 PKCE for Single-Page Applications

Runnable companion files for the recipe [Implement OAuth 2.0 PKCE for Single-Page Applications](https://stackpractices.com/recipes/oauth2-pkce-spa/).

Browser-first implementation of the OAuth 2.0 Authorization Code flow with PKCE (`S256`), `state` validation, silent refresh via hidden iframe, a React `useAuth` hook, and an Express BFF variant that keeps tokens in `httpOnly` cookies.

## Structure

| File | Purpose |
| --- | --- |
| `auth/pkce.ts` | `code_verifier` / `code_challenge` (S256) and random string generation via Web Crypto API |
| `auth/authorize.ts` | Build the authorization URL and start the redirect |
| `auth/tokenExchange.ts` | Callback handling, `state` validation and code → token exchange |
| `auth/storage.ts` | Token storage (module-scoped, never localStorage) |
| `auth/silentRefresh.ts` | Token renewal via hidden iframe with `prompt=none` |
| `public/silent-callback.html` | Silent redirect URI that posts the `code` back to the parent window |
| `server/bff-auth.ts` | Express BFF: PKCE and tokens on the server, `httpOnly` cookies for the SPA |
| `hooks/useAuth.ts` | React hook wiring login, logout, callback and auto-refresh |

## Requirements

- Browser with Web Crypto API (any modern browser, HTTPS or localhost)
- Node 18+ for the BFF example (Express, `cookie-parser`)
- An OAuth 2.0 provider supporting PKCE (Auth0, Keycloak, Entra ID, Cognito...)

## Quick start

1. Copy `auth/` and `public/silent-callback.html` into your SPA.
2. Register `redirectUri` and `silentRedirectUri` in your provider console.
3. Set `authorizationEndpoint`, `tokenEndpoint` and `clientId` in each module (or extract them into a config file).
4. For the BFF variant: `npm i express cookie-parser` and run `server/bff-auth.ts` with `tsx` or `ts-node`.

## Security notes

- PKCE with `S256` is required for public clients — `plain` leaks the verifier.
- `state` prevents login CSRF; always validate it in the callback.
- Access tokens live in memory only; refresh tokens belong in a BFF `httpOnly` cookie, never in `localStorage`.
