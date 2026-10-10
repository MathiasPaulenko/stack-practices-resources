# Handle CORS in Express, Flask and Spring Boot

Companion resource for [Handle CORS in Express, Flask and Spring Boot](https://stackpractices.com/recipes/handle-cors/).

## Files

- `cors_server.py` — Flask API with allowlist CORS middleware and OPTIONS preflight handling.
- `cors-server.mjs` — the same middleware for Express (Node.js).
- `verify-cors.sh` — curl script that checks simple requests, preflight and disallowed origins.
- `requirements.txt`, `package.json` — dependencies.

## Usage

```bash
# Python
pip install -r requirements.txt
python cors_server.py

# or Node.js
npm install
node cors-server.mjs

# Then, from another terminal:
bash verify-cors.sh http://localhost:5000
```

## What it demonstrates

- Reflecting only allowlisted origins in `Access-Control-Allow-Origin`.
- Preflight (`OPTIONS`) responses with allowed methods, headers and `Max-Age`.
- Credentials support (`Access-Control-Allow-Credentials: true`) without the `*` wildcard.
- `Vary: Origin` on responses so shared caches don't mix origins.
