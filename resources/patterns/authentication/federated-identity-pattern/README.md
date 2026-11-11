# Federated Identity Pattern

Delegate authentication to an external identity provider (Google, GitHub, Entra ID, Okta) via OAuth2/OIDC — the app verifies signed tokens and never stores passwords. Companion code for the [Federated Identity Pattern](https://stackpractices.com/patterns/federated-identity-pattern/) article.

## Files

| File | Description |
|------|-------------|
| `python/federated_identity.py` | FastAPI + httpx + PyJWT: authorization-code flow with real JWKS signature validation (`PyJWKClient`) |
| `javascript/federated_identity.js` | Express + `express-openid-connect`: the whole flow (discovery, JWKS, state, sessions) handled by middleware |
| `java/FederatedIdentityApp.java` | Spring Security `oauth2Login` + OIDC-initiated logout that propagates to the IdP |

## Notes

- Replace `your-client-id` / `your-client-secret` with real app credentials; read secrets from env vars in production.
- The Python example validates tokens against the IdP's published JWKS — never ship `verify_signature=False`.
- Dependencies: Python `fastapi httpx pyjwt[crypto]`; Node `express express-openid-connect`; Java `spring-boot-starter-oauth2-client`.
