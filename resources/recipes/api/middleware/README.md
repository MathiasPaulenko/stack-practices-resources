# Middleware — Companion

Runnable companion for the [middleware recipe](https://stackpractices.com/recipes/middleware/) on StackPractices. Working middleware chains that demonstrate the ordering rules from the recipe:

| File | What it is |
|------|------------|
| `express/server.js` | Full chain: logging → CORS → auth (scoped to `/api`) → routes → error handler. Includes `/boom` to trigger the error middleware. |
| `fastapi/main.py` | `@app.middleware` timing logger, `CORSMiddleware`, and a `verify_token` dependency on `/api/protected`. |
| `java/` | The Spring `HandlerInterceptor` + `WebMvcConfigurer` registration is shown in the recipe body — it lives inside a Spring app context, not a standalone file. |

## Run it

```bash
# Express
cd express && npm install && npm start
curl http://localhost:3000/api/protected                      # 401
curl http://localhost:3000/api/protected -H "Authorization: Bearer x"
curl http://localhost:3000/boom                               # error middleware

# FastAPI
cd fastapi && pip install -r requirements.txt && uvicorn main:app --port 8000
curl http://localhost:8000/api/protected                      # 401
curl http://localhost:8000/api/protected -H "Authorization: Bearer x"
```

Source recipe: https://stackpractices.com/recipes/middleware/
