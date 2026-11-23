# supertest Express API Testing — Companion Project

Runnable version of the [Test Express APIs with supertest](https://stackpractices.com/recipes/nodejs-supertest-express-api/) recipe.

## What's inside

- `app.js` — Express app exported via `createApp()`. `listen()` is never called here, so tests can hand the app to supertest without binding a port.
- `server.js` — the only file that calls `app.listen()`, used for real deployments.
- `api.test.js` — supertest + Vitest suite covering health checks, POST validation, pagination, JWT auth (valid/expired/missing), cookie sessions via `request.agent`, and error middleware.
- `package.json` — dependencies: express 4, jsonwebtoken, supertest 7, vitest 3.

## Run it

```bash
npm install
npm test       # vitest run — all supertest assertions
npm start      # real server on :3000
```

## Notes

- `request(app)` spins an ephemeral HTTP server per request — no port collisions in CI.
- `request.agent(app)` persists cookies between calls (see the session test).
