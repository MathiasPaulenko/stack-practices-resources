# Manejar Errores en APIs con RFC 7807 — Recursos Companion

Código companion de la receta [Manejar Errores en APIs con RFC 7807](https://stackpractices.com/es/recipes/handle-errors/) en StackPractices.

## Contenidos

| Archivo | Lenguaje | Framework | Descripción |
| --- | --- | --- | --- |
| `python_fastapi.py` | Python | FastAPI | Server con exception handlers de Problem Details |
| `javascript_express.js` | JavaScript | Express | Server con middleware de error global |
| `java_spring_boot.java` | Java | Spring Boot | Controller + handler `@ControllerAdvice` |
| `test_errors.py` | Python | pytest | Contract tests del shape Problem Details |
| `test_errors.js` | JavaScript | Jest + supertest | Contract tests del shape Problem Details |
| `requirements.txt` | Python | — | Dependencias de Python |
| `package.json` | JavaScript | — | Dependencias y scripts de Node |
| `pom.xml` | Java | Maven | Configuración del proyecto Maven |

## Ejecutar el server de Python

```bash
pip install -r requirements.txt
python python_fastapi.py
# Server en http://127.0.0.1:8000
```

## Ejecutar el server de JavaScript

```bash
npm install
npm start
# Server en http://localhost:3000
```

## Ejecutar tests

### Python

```bash
pip install -r requirements.txt
pytest test_errors.py -v
```

### JavaScript

```bash
npm install
npm test
```

## Shape de RFC 7807 Problem Details

Todos los servers devuelven errores en este formato con `Content-Type: application/problem+json`:

```json
{
  "type": "https://api.example.com/errors/not-found",
  "title": "User Not Found",
  "status": 404,
  "detail": "No user with id 42",
  "instance": "/users/42"
}
```

## Referencias

- [RFC 7807](https://datatracker.ietf.org/doc/html/rfc7807) — Problem Details for HTTP APIs
- [RFC 9457](https://www.rfc-editor.org/rfc/rfc9457) — Especificación sucesora
- [MDN HTTP Status Codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)
