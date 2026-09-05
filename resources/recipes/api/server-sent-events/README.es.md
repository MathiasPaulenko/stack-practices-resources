# Server-Sent Events (SSE) — Recursos Companion

Ejemplos ejecutables para la receta [Server-Sent Events](https://stackpractices.com/es/recipes/server-sent-events/) en StackPractices.

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `server.py` | Servidor SSE con Flask y broadcasting |
| `server.js` | Servidor SSE con Express y broadcasting |
| `Server.java` | Servidor SSE con Spring Boot |
| `client.html` | Demo de cliente del navegador |
| `redis_pubsub.py` | Servidor SSE con Flask y escalado via Redis pub/sub |
| `nginx.conf` | Config de proxy Nginx con buffering SSE deshabilitado |
| `docker-compose.yml` | Docker Compose con Redis + servidor SSE + Nginx |
| `Dockerfile` | Imagen Docker para el servidor SSE en Python |

## Inicio rápido

### Python (Flask)

```bash
pip install flask
python server.py
# Abrí http://localhost:5000/events en un navegador o:
curl -N http://localhost:5000/events
```

### Node.js (Express)

```bash
npm install express
node server.js
# Abrí http://localhost:3000/events
curl -N http://localhost:3000/events
```

### Java (Spring Boot)

```bash
javac Server.java && java -cp .:spring-boot-starter-web.jar Server
# Abrí http://localhost:8080/events
```

### Docker Compose (con Redis pub/sub + Nginx)

```bash
docker-compose up -d
# Endpoint SSE: http://localhost:8080/events
# Publicar: curl http://localhost:8080/publish/hello
```

## Testing

```bash
# Testear stream SSE
curl -N -H "Accept: text/event-stream" http://localhost:5000/events

# Publicar un mensaje a todos los clientes de broadcast
curl http://localhost:5000/publish/hello-world

# Verificar que los eventos llegan de a uno (no bufferizados)
curl -N http://localhost:5000/events | while read line; do echo "$(date): $line"; done
```
