# Seguimiento de Errores con Sentry en Express

Repositorio complementario de la receta [Seguimiento de Errores con Sentry en Express](https://stackpractices.com/es/recipes/nodejs-sentry-error-tracking/) de StackPractices.

## Archivos

- `instrument.js` — inicialización de Sentry v8+ (se carga antes de la app)
- `app.js` — app Express con `setupExpressErrorHandler`, contexto de usuario, breadcrumbs y un `startSpan` personalizado
- `package.json` — dependencias mínimas (`@sentry/node` v8+, `express`)
- `.env.example` — variables de entorno (`SENTRY_DSN`, `SENTRY_RELEASE`, `NODE_ENV`)

## Inicio rápido

```bash
npm install
cp .env.example .env   # rellena tu SENTRY_DSN
npm start
```

Después dispara el error de prueba:

```bash
curl http://localhost:3000/debug-sentry
```

El evento debería aparecer en tu panel de Sentry en segundos, con el contexto de la petición, el usuario `alice` y los breadcrumbs.

## Notas

- `require("./instrument")` debe ser el primer import — el SDK parchea `http` y `express` al cargarse. Importarlo tarde hace que los errores pasen sin reportar.
- `setupExpressErrorHandler` solo captura errores 5xx por defecto; los 4xx se consideran errores de cliente esperados. Personalízalo con `Sentry.expressIntegration({ shouldHandleError })`.
- Express 4 no reenvía las promesas rechazadas de los handlers `async` al middleware de error — envuélvelos o usa `next(err)`. Express 5 lo hace de forma nativa.
