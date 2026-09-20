# Respuestas de Error de API — Recursos Companion

Companion ejecutable del documento **[Plantilla de Respuesta de Error de API](https://stackpractices.com/es/docs/api-error-response-template/)** en StackPractices.

## Archivos

| Archivo | Propósito |
|---|---|
| `error-responses.json` | Catálogo de errores legible por máquina (status → code → type/title/when). Genera docs, handlers y contract tests desde esta única fuente. |
| `problem-details.js` | Middleware de Express que emite `application/problem+json` RFC 9457: clase `ApiError` + handler catch-all con request IDs, 500s sanitizados y `errors` a nivel de campo. |
| `problem_details.py` | Equivalente en Flask: `ApiError` + `register_problem_details(app)` con paso de `X-Request-ID` y logging del contexto de los 5xx. |

## Inicio rápido — Express

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
curl -i http://localhost:3000/crash   # 500, cuerpo sanitizado, request_id para logs
```

## Inicio rápido — Flask

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

## Notas

- `API_ERRORS_BASE_URI` sobrescribe el prefijo del URI `type` en ambas implementaciones.
- La rama 500 nunca repite `err.message` — solo las instancias de `ApiError` llegan al cuerpo. Todo lo demás se loguea en el servidor con el `request_id` que ve el cliente.
- Extiende `error-responses.json` con tus propios códigos; nunca recicles un `code` retirado para un significado distinto.
