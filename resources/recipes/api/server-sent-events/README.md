# Server-Sent Events (SSE) — Companion Resources

Runnable examples for the [Server-Sent Events](https://stackpractices.com/recipes/server-sent-events/) recipe on StackPractices.

## Files

| File | Purpose |
|------|---------|
| `server.py` | Flask SSE server with broadcasting |
| `server.js` | Express SSE server with broadcasting |
| `Server.java` | Spring Boot SSE server |
| `client.html` | Browser client demo |
| `redis_pubsub.py` | Flask SSE server with Redis pub/sub scaling |
| `nginx.conf` | Nginx proxy config with SSE buffering disabled |
| `docker-compose.yml` | Docker Compose with Redis + SSE server + Nginx |
| `Dockerfile` | Docker image for the Python SSE server |

## Quick start

### Python (Flask)

```bash
pip install flask
python server.py
# Open http://localhost:5000/events in a browser or:
curl -N http://localhost:5000/events
```

### Node.js (Express)

```bash
npm install express
node server.js
# Open http://localhost:3000/events
curl -N http://localhost:3000/events
```

### Java (Spring Boot)

```bash
javac Server.java && java -cp .:spring-boot-starter-web.jar Server
# Open http://localhost:8080/events
```

### Docker Compose (with Redis pub/sub + Nginx)

```bash
docker-compose up -d
# SSE endpoint: http://localhost:8080/events
# Publish: curl http://localhost:8080/publish/hello
```

## Testing

```bash
# Test SSE stream
curl -N -H "Accept: text/event-stream" http://localhost:5000/events

# Publish a message to all broadcast clients
curl http://localhost:5000/publish/hello-world

# Check that events arrive one at a time (not buffered)
curl -N http://localhost:5000/events | while read line; do echo "$(date): $line"; done
```
