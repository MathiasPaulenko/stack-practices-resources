# Node.js JWT Authentication

Companion project for the recipe [Node.js JWT Authentication](https://stackpractices.com/recipes/nodejs-jwt-authentication/).

A runnable Express server that chains all the recipe snippets into one app: bcrypt login, short-lived access tokens, refresh token rotation with reuse detection, family revocation, logout, and a protected route guarded by JWT middleware.

## Contents

| File | What it does |
| ---- | ------------ |
| `server.js` | Express app: `/auth/login`, `/auth/refresh` (rotation + reuse detection), `/auth/logout`, `/api/profile` (protected) |
| `test.js` | `node:test` flow test — spins the server up and walks login → protected route → rotation → reuse detection → logout |
| `package.json` | Dependencies: `express`, `jsonwebtoken`, `bcrypt` |

## Run it

```bash
npm install
npm start

# in another terminal
curl -X POST http://localhost:3000/auth/login \
  -H "content-type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

Use the returned `accessToken` against `GET /api/profile` (`Authorization: Bearer …`) and the `refreshToken` against `POST /auth/refresh`. Re-presenting a consumed refresh token returns `401` with `code: "reuse_detected"` and revokes the whole token family — try replaying the old token after a refresh.

## Test it

```bash
npm test
```

One test covers the full flow: bad password → login → protected route with and without token → rotation → reuse detection → family revocation → logout.

## Notes

- The demo user `admin`/`admin123` is hashed with bcrypt at startup — replace the `users` array with a real user store.
- `ACCESS_TOKEN_SECRET`/`REFRESH_TOKEN_SECRET` fall back to dev strings so the demo runs; in production load them from env vars and fail fast if missing.
- The refresh store is an in-memory `Map` keyed by `jti` so the demo needs no Redis; move it to Redis with a TTL for multi-instance deployments.
