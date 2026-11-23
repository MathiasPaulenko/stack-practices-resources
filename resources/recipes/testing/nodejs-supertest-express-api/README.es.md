# Testing de API Express con supertest — Proyecto complementario

Versión ejecutable de la receta [Testear APIs Express con supertest](https://stackpractices.com/es/recipes/nodejs-supertest-express-api/).

## Qué incluye

- `app.js` — app Express exportada vía `createApp()`. Nunca se llama a `listen()` aquí, así que los tests pueden pasar la app a supertest sin bindear un puerto.
- `server.js` — el único archivo que llama a `app.listen()`, pensado para despliegues reales.
- `api.test.js` — suite supertest + Vitest que cubre health checks, validación de POST, paginación, auth JWT (válido/expirado/ausente), sesiones con cookie vía `request.agent` y el middleware de errores.
- `package.json` — dependencias: express 4, jsonwebtoken, supertest 7, vitest 3.

## Ejecutarlo

```bash
npm install
npm test       # vitest run — todas las aserciones de supertest
npm start      # servidor real en :3000
```

## Notas

- `request(app)` levanta un servidor HTTP efímero por petición — sin colisiones de puertos en CI.
- `request.agent(app)` persiste las cookies entre llamadas (ver el test de sesión).
