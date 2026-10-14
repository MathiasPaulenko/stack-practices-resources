# Fast Structured Logging with pino

Runnable companion code for the StackPractices recipe
[High-Performance Logging with pino](https://stackpractices.com/recipes/nodejs-pino-fast-logging/).

## Files

| File | What it shows |
|------|---------------|
| `logger.js` | Shared pino config: `LOG_LEVEL` env, `base` fields, `redact` paths, dev-only `pino-pretty` transport |
| `express-app.js` | Express + `pino-http` request logging, `genReqId` request ids, error handler logging |
| `fastify-app.js` | Fastify with its built-in pino logger |
| `package.json` | Dependencies and start scripts |

## Run

```bash
npm install
npm run start:express   # http://localhost:3000/api/users/42
npm run start:fastify   # http://localhost:3001/api/users/42
npm run dev             # Express with pino-pretty output
```

Pretty output without the dependency:

```bash
node express-app.js | npx pino-pretty
```

## Key detail

pino's signature is `logger.info(mergingObject, "message")` — the object comes
first. The Winston-style order `logger.info("msg", { obj })` silently drops the
fields (the object is treated as a printf argument with no `%j` placeholder).
Every call in these examples uses the correct order.
