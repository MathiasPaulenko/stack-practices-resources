# Patrón Federated Identity

Delega la autenticación a un proveedor de identidad externo (Google, GitHub, Entra ID, Okta) vía OAuth2/OIDC — la app verifica tokens firmados y nunca almacena contraseñas. Código complementario del artículo [Patrón Federated Identity](https://stackpractices.com/es/patterns/federated-identity-pattern/).

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `python/federated_identity.py` | FastAPI + httpx + PyJWT: flujo authorization-code con validación de firma JWKS real (`PyJWKClient`) |
| `javascript/federated_identity.js` | Express + `express-openid-connect`: todo el flujo (discovery, JWKS, state, sesiones) resuelto por middleware |
| `java/FederatedIdentityApp.java` | Spring Security `oauth2Login` + logout iniciado por OIDC que se propaga al IdP |

## Notas

- Sustituye `your-client-id` / `your-client-secret` por credenciales reales de la app; lee los secretos de variables de entorno en producción.
- El ejemplo Python valida tokens contra las JWKS publicadas por el IdP — nunca envíes `verify_signature=False`.
- Dependencias: Python `fastapi httpx pyjwt[crypto]`; Node `express express-openid-connect`; Java `spring-boot-starter-oauth2-client`.
