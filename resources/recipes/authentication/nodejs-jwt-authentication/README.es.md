# Autenticación JWT en Node.js

Proyecto complementario de la receta [Autenticación JWT en Node.js](https://stackpractices.com/es/recipes/nodejs-jwt-authentication/).

Un servidor Express ejecutable que encadena todos los snippets de la receta en una sola app: login con bcrypt, access tokens de corta duración, rotación de refresh tokens con detección de reuso, revocación de familia, logout y una ruta protegida con middleware JWT.

## Contenido

| Archivo | Qué hace |
| ------- | -------- |
| `server.js` | App Express: `/auth/login`, `/auth/refresh` (rotación + detección de reuso), `/auth/logout`, `/api/profile` (protegida) |
| `test.js` | Test de flujo con `node:test` — levanta el servidor y recorre login → ruta protegida → rotación → detección de reuso → logout |
| `package.json` | Dependencias: `express`, `jsonwebtoken`, `bcrypt` |

## Ejecutarlo

```bash
npm install
npm start

# en otra terminal
curl -X POST http://localhost:3000/auth/login \
  -H "content-type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

Usa el `accessToken` devuelto contra `GET /api/profile` (`Authorization: Bearer …`) y el `refreshToken` contra `POST /auth/refresh`. Presentar de nuevo un refresh token ya consumido devuelve `401` con `code: "reuse_detected"` y revoca toda la familia de tokens — probá reintentar el token viejo después de un refresh.

## Probarlo

```bash
npm test
```

Un solo test cubre el flujo completo: contraseña incorrecta → login → ruta protegida con y sin token → rotación → detección de reuso → revocación de familia → logout.

## Notas

- El usuario demo `admin`/`admin123` se hashea con bcrypt al arrancar — reemplazá el array `users` por un store de usuarios real.
- `ACCESS_TOKEN_SECRET`/`REFRESH_TOKEN_SECRET` tienen fallbacks de desarrollo para que el demo corra; en producción cargalos desde variables de entorno y fallá rápido si faltan.
- El store de refresh es un `Map` en memoria indexado por `jti` para no necesitar Redis; movelo a Redis con TTL para despliegues multi-instancia.
