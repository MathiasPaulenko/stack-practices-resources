# Session Management — Secure Sessions Examples

Runnable examples for the [Secure Session Management](https://stackpractices.com/recipes/session-management/) recipe on StackPractices.

## Contents

| File | What it is |
|------|------------|
| `express_sessions.js` | Express + express-session + connect-redis v7: cookie flags, session regeneration on login, logout |
| `SessionConfig.java` | Spring Boot with `@EnableRedisHttpSession` + logout endpoint |
| `concurrent_sessions.py` | Cap active sessions per user in Redis, evicting and deleting the oldest |
| `fastapi_jwt.py` | Stateless JWT variant for non-browser clients |
| `requirements.txt` | Python dependencies |
| `package.json` | Node.js dependencies |

## Quick start

Redis running locally (e.g. `docker run -p 6379:6379 redis`).

Express:

```bash
npm install
npm start            # http://localhost:3000 — POST /login with demo@example.com / demo
```

Python:

```bash
pip install -r requirements.txt
python concurrent_sessions.py   # evicts the oldest session past the cap
```
