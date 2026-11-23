# OAuth 2.0 PKCE para aplicaciones de una sola página

Archivos ejecutables que acompañan a la receta [Implementa OAuth 2.0 PKCE para aplicaciones de una sola página](https://stackpractices.com/es/recipes/oauth2-pkce-spa/).

Implementación browser-first del flujo de código de autorización de OAuth 2.0 con PKCE (`S256`), validación de `state`, renovación silenciosa vía iframe oculto, hook de React `useAuth` y una variante BFF en Express que guarda los tokens en cookies `httpOnly`.

## Estructura

| Archivo | Propósito |
| --- | --- |
| `auth/pkce.ts` | Generación de `code_verifier` / `code_challenge` (S256) y strings aleatorios con Web Crypto API |
| `auth/authorize.ts` | Construir la URL de autorización e iniciar el redirect |
| `auth/tokenExchange.ts` | Manejo del callback, validación de `state` e intercambio código → token |
| `auth/storage.ts` | Almacenamiento de tokens (en módulo, nunca localStorage) |
| `auth/silentRefresh.ts` | Renovación de tokens con iframe oculto y `prompt=none` |
| `public/silent-callback.html` | Redirect URI silenciosa que devuelve el `code` a la ventana padre |
| `server/bff-auth.ts` | BFF en Express: PKCE y tokens en el servidor, cookies `httpOnly` para la SPA |
| `hooks/useAuth.ts` | Hook de React que conecta login, logout, callback y auto-renovación |

## Requisitos

- Navegador con Web Crypto API (cualquier navegador moderno, HTTPS o localhost)
- Node 18+ para el ejemplo BFF (Express, `cookie-parser`)
- Un proveedor OAuth 2.0 con soporte PKCE (Auth0, Keycloak, Entra ID, Cognito...)

## Inicio rápido

1. Copia `auth/` y `public/silent-callback.html` a tu SPA.
2. Registra `redirectUri` y `silentRedirectUri` en la consola de tu proveedor.
3. Configura `authorizationEndpoint`, `tokenEndpoint` y `clientId` en cada módulo (o extráelos a un archivo de configuración).
4. Para la variante BFF: `npm i express cookie-parser` y ejecuta `server/bff-auth.ts` con `tsx` o `ts-node`.

## Notas de seguridad

- PKCE con `S256` es obligatorio para clientes públicos: `plain` expone el verifier.
- `state` previene CSRF de login; valídalo siempre en el callback.
- Los access tokens viven solo en memoria; los refresh tokens van en una cookie `httpOnly` del BFF, nunca en `localStorage`.
