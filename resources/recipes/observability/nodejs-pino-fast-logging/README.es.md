# Logging Estructurado Rápido con pino

Código ejecutable que acompaña a la receta de StackPractices
[Logging de Alta Performance con pino](https://stackpractices.com/es/recipes/nodejs-pino-fast-logging/).

## Archivos

| Archivo | Qué muestra |
|---------|-------------|
| `logger.js` | Config pino compartida: `LOG_LEVEL` por env, campos `base`, paths de `redact`, transport `pino-pretty` solo en desarrollo |
| `express-app.js` | Express + `pino-http` con logging de requests, `genReqId` para request ids y logging en el manejador de errores |
| `fastify-app.js` | Fastify con su logger pino integrado |
| `package.json` | Dependencias y scripts de arranque |

## Ejecutar

```bash
npm install
npm run start:express   # http://localhost:3000/api/users/42
npm run start:fastify   # http://localhost:3001/api/users/42
npm run dev             # Express con salida pino-pretty
```

Salida legible sin la dependencia:

```bash
node express-app.js | npx pino-pretty
```

## Detalle clave

La firma de pino es `logger.info(mergingObject, "message")` — el objeto va
primero. El orden estilo Winston `logger.info("msg", { obj })` descarta los
campos en silencio (el objeto se trata como argumento printf sin placeholder
`%j`). Todas las llamadas de estos ejemplos usan el orden correcto.
