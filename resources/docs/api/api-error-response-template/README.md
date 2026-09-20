# API Error Response — Companion Resources

Runnable companion for the doc **[API Error Response Template](https://stackpractices.com/docs/api-error-response-template/)** on StackPractices.

## Files

| File | Purpose |
|---|---|
| `error-responses.json` | Machine-readable error catalog (status → code → type/title/when). Generate docs, handlers, and contract tests from this single source. |
| `problem-details.js` | Express middleware emitting RFC 9457 `application/problem+json`: `ApiError` class + catch-all handler with request IDs, sanitized 500s, and field-level `errors`. |
| `problem_details.py` | Flask equivalent: `ApiError` + `register_problem_details(app)` with `X-Request-ID` passthrough and logging of 5xx context. |

## Quick start — Express

```bash
npm install express
node -e "
const express = require('express');
const { ApiError, problemDetails } = require('./problem-details');
const app = express();
app.use((req, res, next) => { req.id = 'req_demo'; next(); });
app.get('/boom', () => { throw new ApiError(429, 'https://api.example.com/errors/rate-limit-exceeded', 'Rate Limit Exceeded', 'Retry after 30 seconds.'); });
app.get('/crash', () => { throw new Error('db connection lost'); });
app.use(problemDetails);
app.listen(3000);
" &
curl -i http://localhost:3000/boom    # 429 + application/problem+json
curl -i http://localhost:3000/crash   # 500, sanitized body, request_id for logs
```

## Quick start — Flask

```bash
pip install flask
python -c "
from flask import Flask
from problem_details import ApiError, register_problem_details
app = Flask(__name__)
register_problem_details(app)

@app.get('/boom')
def boom():
    raise ApiError(429, 'https://api.example.com/errors/rate-limit-exceeded',
                   'Rate Limit Exceeded', 'Retry after 30 seconds.')

app.run(port=3000)
" &
curl -i http://localhost:3000/boom
```

## Notes

- `API_ERRORS_BASE_URI` overrides the `type` URI prefix in both implementations.
- The 500 branch never echoes `err.message` — only `ApiError` instances reach the body. Everything else logs server-side with the `request_id` the client sees.
- Extend `error-responses.json` with your own codes; never recycle a retired `code` for a different meaning.
