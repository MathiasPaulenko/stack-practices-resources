# Notificaciones en tiempo real con WebSockets — Recursos complementarios

Archivos complementarios de [Construir notificaciones en tiempo real con WebSockets](https://stackpractices.com/es/recipes/real-time-notifications/) en StackPractices.

## Archivos

| Archivo | Qué demuestra |
|---------|---------------|
| `server.js` | Servidor WebSocket con enrutado por rooms y fan-out por Redis pub/sub entre instancias |
| `client.html` | Cliente de navegador que se une a un room, muestra notificaciones y reconecta con backoff exponencial |
| `publish.js` | CLI que publica un mensaje `{room, text}` en el canal `notifications` |
| `package.json` | Dependencias (`ws`, `ioredis`) y scripts de arranque |
| `docker-compose.yml` | Redis 7 de un solo servicio para pruebas locales |

## Cómo usarlo

```bash
docker compose up -d        # arranca Redis
npm install                 # instala ws + ioredis
npm start                   # arranca el servidor WebSocket en :8080
```

Abre `client.html` en el navegador (opcionalmente con `?room=orders` en la URL) y desde otra terminal:

```bash
node publish.js orders "¡Nuevo pedido!"   # envía una notificación al room
```

Para ver el fan-out entre instancias, ejecuta `PORT=8081 node server.js` junto a la instancia por defecto — un publish alcanza a los clientes de ambas.

Sin dependencias más allá de Node.js ≥ 18, Docker y los dos paquetes npm.
