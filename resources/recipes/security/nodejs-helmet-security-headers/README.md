# Helmet Security Headers — Companion Code

Runnable Express app with Helmet 8 security headers, from the StackPractices recipe:
[Configure HTTP Security Headers with Helmet in Node.js](https://stackpractices.com/recipes/nodejs-helmet-security-headers/)

## Files

| File | Purpose |
| --- | --- |
| `app.js` | Express app with Helmet CSP, HSTS, X-Frame-Options and CORS configured |
| `server.js` | Entry point — listens on `PORT` (default 3000) |
| `headers.test.js` | Jest + supertest suite asserting each security header |
| `package.json` | Dependencies: express 4, helmet 8, cors; devDeps: jest, supertest |

## Run

```bash
npm install
npm start          # http://localhost:3000
npm test           # runs the header assertions
```

Verify headers against the running server:

```bash
curl -sI http://localhost:3000 | grep -iE "strict-transport|x-frame|x-content|content-security"
```
