# Llamar a una API REST — Ejemplos Companion

Ejemplos runnable de clientes HTTP que acompañan la receta de StackPractices
[Llamar a una API REST: Python, JS, Java y Go](https://stackpractices.com/es/recipes/call-rest-api/).

## Archivos

| Archivo | Lenguaje | Qué hace |
|---------|----------|----------|
| `get_request.py` | Python | GET con `requests`, timeout, `raise_for_status`, manejo de errores |
| `post_request.py` | Python | POST con Bearer auth, JSON body, API key desde env var |
| `fetch_get.js` | JavaScript | GET con `fetch`, verificación de `response.ok`, parseo JSON |
| `fetch_timeout.js` | JavaScript | GET con `AbortController` timeout (10s) |
| `httpclient_get.java` | Java | GET con `HttpClient` (Java 11+), timeout de conexión y lectura |
| `nethttp_get.go` | Go | GET con `net/http`, `context` timeout, cierre de body |

## Ejecución

### Python

```bash
pip install requests
python get_request.py
API_KEY=tu_key python post_request.py
```

### JavaScript (Node.js 18+)

```bash
node fetch_get.js
node fetch_timeout.js
```

### Java (11+)

```bash
javac httpclient_get.java
java httpclient_get
```

### Go

```bash
go run nethttp_get.go
```

## Notas

- Todos los ejemplos usan `https://api.example.com` como placeholder. Reemplazá con una URL real.
- El ejemplo POST de Python lee `API_KEY` de una variable de entorno. Nunca hardcodees credenciales.
- Los timeouts están seteados en 10 segundos. Ajustá según el SLA de tu API.
