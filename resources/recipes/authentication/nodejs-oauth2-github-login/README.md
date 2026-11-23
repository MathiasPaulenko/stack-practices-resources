# Node.js OAuth2 GitHub Login with Express

Companion project for the [StackPractices recipe](https://stackpractices.com/recipes/nodejs-oauth2-github-login/).

A runnable Express app implementing the GitHub OAuth2 authorization code flow
with state verification and `access_denied` handling. It ships with a local
GitHub stub so you can run the entire flow end-to-end without registering a
real OAuth App.

## Files

| File | Purpose |
| --- | --- |
| `server.js` | Express app: `/auth/github` redirect, state check, code exchange, session login, `/profile`, `/auth/logout` |
| `github-stub.js` | Minimal GitHub OAuth provider stub (authorize, token, `/user`, `/user/emails`) |
| `test.js` | `node:test` end-to-end suite covering the happy path, forged state rejection, and the denial case |
| `package.json` | `express` + `express-session`; `npm test` runs the suite |

## Run it

```bash
npm install

# Terminal 1 — fake GitHub provider
npm run stub          # listens on :4000

# Terminal 2 — the app, pointed at the stub
GITHUB_WEB=http://localhost:4000 GITHUB_API=http://localhost:4000 npm start
```

Then open `http://localhost:3000` and click "Login with GitHub" — the stub
approves instantly and you land on `/profile` with a stub user.

## Run the tests

```bash
npm test
```

Two tests: the full authorize → callback → profile → logout flow (including
forged-state rejection), and the `error=access_denied` path.

## Real GitHub

Create an OAuth App under *Settings > Developer settings > OAuth Apps* with
callback `http://localhost:3000/auth/github/callback`, then run without the
stub variables:

```bash
GITHUB_CLIENT_ID=xxx GITHUB_CLIENT_SECRET=yyy npm start
```

`server.js` defaults `githubWeb`/`githubApi` to the real GitHub endpoints.
