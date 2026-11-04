# OAuth2/OIDC en Producción — Companion

Módulos TypeScript ejecutables de la [Guía Completa de OAuth2 y OIDC en Producción](https://stackpractices.com/es/guides/complete-guide-oauth2-oidc-production/).

## Archivos

- `pkce.ts` — generación del par verifier/challenge de PKCE (RFC 7636)
- `env.ts` — helper de variables de entorno que falla rápido al arrancar
- `authorize.ts` — constructor de la URL de autorización (`response_type=code`, `S256`, `state`, `offline_access`)
- `callback.ts` — handler del callback: validación de `state` en tiempo constante + intercambio del código + sesión
- `jwt.ts` — validación de access tokens contra JWKS + `authMiddleware` (jsonwebtoken + jwks-rsa)
- `oidc.ts` — validación asíncrona del ID token: firma, `aud`, `nonce` y claims OIDC requeridos
- `refresh.ts` — grant de refresh con rotación + middleware de renovación (buffer de 60s)
- `scopes.ts` — middleware `requireScope` que devuelve `insufficient_scope` (RFC 6750)
- `discovery.ts` — fetch del discovery document OIDC + config tipada
- `clientCredentials.ts` — grant client-credentials M2M
- `revoke.ts` — revocación de tokens (RFC 7009)
- `introspect.ts` — introspección para tokens opacos (RFC 7662)

## Uso

```bash
npm install
npx tsc
```

Configurá `OAUTH_CLIENT_ID`, `OAUTH_CLIENT_SECRET`, `M2M_CLIENT_ID`, `M2M_CLIENT_SECRET` y apuntá `auth.example.com` a tu IdP antes de conectar `callback.ts`, `jwt.ts`, `oidc.ts`, `refresh.ts` y `scopes.ts` a una app Express.

## Requisitos

- Node.js 18+ (`fetch` nativo)
- `jsonwebtoken`, `jwks-rsa`, `express`, `express-session`
