# Handle API Errors with RFC 7807 — Companion Resources

Companion code for the [Handle API Errors with RFC 7807](https://stackpractices.com/recipes/handle-errors/) recipe on StackPractices.

## Contents

| File | Language | Framework | Description |
| --- | --- | --- | --- |
| `python_fastapi.py` | Python | FastAPI | Server with Problem Details exception handlers |
| `javascript_express.js` | JavaScript | Express | Server with global error middleware |
| `java_spring_boot.java` | Java | Spring Boot | Controller + `@ControllerAdvice` handler |
| `test_errors.py` | Python | pytest | Contract tests for Problem Details shape |
| `test_errors.js` | JavaScript | Jest + supertest | Contract tests for Problem Details shape |
| `requirements.txt` | Python | — | Python dependencies |
| `package.json` | JavaScript | — | Node dependencies and scripts |
| `pom.xml` | Java | Maven | Maven project configuration |

## Running the Python server

```bash
pip install -r requirements.txt
python python_fastapi.py
# Server runs on http://127.0.0.1:8000
```

## Running the JavaScript server

```bash
npm install
npm start
# Server runs on http://localhost:3000
```

## Running tests

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

## RFC 7807 Problem Details shape

All servers return errors in this format with `Content-Type: application/problem+json`:

```json
{
  "type": "https://api.example.com/errors/not-found",
  "title": "User Not Found",
  "status": 404,
  "detail": "No user with id 42",
  "instance": "/users/42"
}
```

## References

- [RFC 7807](https://datatracker.ietf.org/doc/html/rfc7807) — Problem Details for HTTP APIs
- [RFC 9457](https://www.rfc-editor.org/rfc/rfc9457) — Successor specification
- [MDN HTTP Status Codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)
