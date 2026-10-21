# Middleware — Companion

Companion ejecutable de la [receta de middleware](https://stackpractices.com/es/recipes/middleware/) en StackPractices. Cadenas de middleware funcionales que demuestran las reglas de orden de la receta:

| Archivo | Qué es |
|---------|--------|
| `express/server.js` | Cadena completa: logging → CORS → auth (limitado a `/api`) → rutas → error handler. Incluye `/boom` para disparar el middleware de errores. |
| `fastapi/main.py` | Logger de timing con `@app.middleware`, `CORSMiddleware` y una dependencia `verify_token` en `/api/protected`. |
| `java/` | El `HandlerInterceptor` de Spring + el registro `WebMvcConfigurer` aparecen en la receta — viven dentro del contexto de una app Spring, no en un archivo aparte. |

## Ejecutarlo

```bash
# Express
cd express && npm install && npm start
curl http://localhost:3000/api/protected                      # 401
curl http://localhost:3000/api/protected -H "Authorization: Bearer x"
curl http://localhost:3000/boom                               # middleware de errores

# FastAPI
cd fastapi && pip install -r requirements.txt && uvicorn main:app --port 8000
curl http://localhost:8000/api/protected                      # 401
curl http://localhost:8000/api/protected -H "Authorization: Bearer x"
```

Receta original: https://stackpractices.com/es/recipes/middleware/
