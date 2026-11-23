# Login con OAuth2 de GitHub en Node.js con Express

Proyecto companion de la [recipe de StackPractices](https://stackpractices.com/es/recipes/nodejs-oauth2-github-login/).

Una app Express ejecutable que implementa el authorization code flow de GitHub
OAuth2 con verificación de state y manejo de `access_denied`. Incluye un stub
local de GitHub para correr todo el flujo end-to-end sin registrar una OAuth
App real.

## Archivos

| Archivo | Propósito |
| --- | --- |
| `server.js` | App Express: redirect de `/auth/github`, verificación de state, intercambio del code, login por sesión, `/profile`, `/auth/logout` |
| `github-stub.js` | Stub mínimo del proveedor OAuth de GitHub (authorize, token, `/user`, `/user/emails`) |
| `test.js` | Suite end-to-end con `node:test` que cubre el camino feliz, el rechazo de state forjado y el caso de denegación |
| `package.json` | `express` + `express-session`; `npm test` corre la suite |

## Ejecutar

```bash
npm install

# Terminal 1 — proveedor GitHub falso
npm run stub          # escucha en :4000

# Terminal 2 — la app, apuntando al stub
GITHUB_WEB=http://localhost:4000 GITHUB_API=http://localhost:4000 npm start
```

Después abrí `http://localhost:3000` y hacé clic en "Login with GitHub" — el
stub aprueba al instante y caés en `/profile` con un usuario de prueba.

## Correr los tests

```bash
npm test
```

Dos tests: el flujo completo authorize → callback → profile → logout (incluido
el rechazo de state forjado), y el camino de `error=access_denied`.

## GitHub real

Creá una OAuth App en *Settings > Developer settings > OAuth Apps* con callback
`http://localhost:3000/auth/github/callback`, y corré sin las variables del
stub:

```bash
GITHUB_CLIENT_ID=xxx GITHUB_CLIENT_SECRET=yyy npm start
```

`server.js` usa por defecto los endpoints reales de GitHub en
`githubWeb`/`githubApi`.
