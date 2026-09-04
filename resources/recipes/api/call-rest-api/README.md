# Call a REST API — Companion Examples

Runnable HTTP client examples accompanying the StackPractices recipe
[Call a REST API: Python, JavaScript, Java & Go Examples](https://stackpractices.com/recipes/call-rest-api/).

## Files

| File | Language | What it does |
|------|----------|-------------|
| `get_request.py` | Python | GET with `requests`, timeout, `raise_for_status`, error handling |
| `post_request.py` | Python | POST with Bearer auth, JSON body, env var for API key |
| `fetch_get.js` | JavaScript | GET with `fetch`, `response.ok` check, JSON parse |
| `fetch_timeout.js` | JavaScript | GET with `AbortController` timeout (10s) |
| `httpclient_get.java` | Java | GET with `HttpClient` (Java 11+), connect + read timeout |
| `nethttp_get.go` | Go | GET with `net/http`, `context` timeout, body close |

## Running

### Python

```bash
pip install requests
python get_request.py
API_KEY=your_key python post_request.py
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

## Notes

- All examples use `https://api.example.com` as a placeholder. Replace with a real API URL.
- The Python POST example reads `API_KEY` from an environment variable. Never hardcode credentials.
- Timeouts are set to 10 seconds. Adjust based on your API's SLA.
