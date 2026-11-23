# Chat en tiempo real con Socket.io — Proyecto complementario

Complemento ejecutable de la receta de StackPractices [Comunicación en Tiempo Real con WebSocket y Socket.io en Node.js](https://stackpractices.com/es/recipes/nodejs-websocket-realtime/).

## Qué incluye

- `server.js` — servidor de chat Express + Socket.io: registro de usuarios, rooms (`join-room`/`leave-room`/`room-message`), broadcasting, indicadores de escritura y limpieza de presencia en `disconnect`.
- `client.js` — cliente Socket.io para Node que se une, envía mensajes cada 5s e imprime el tráfico del chat. Ejecuta dos instancias para ver la entrega en tiempo real.

## Ejecución

```bash
npm install
npm start          # servidor en :3000

# en otra terminal
npm run client     # o: USERNAME=bob node client.js
# y otra más
USERNAME=alice node client.js
```

## Opcional: Redis adapter para escalar a varias instancias

El `package.json` incluye `@socket.io/redis-adapter` e `ioredis` como dependencias opcionales. Para escalar entre instancias:

```javascript
import { createAdapter } from "@socket.io/redis-adapter";
import { Redis } from "ioredis";

const pubClient = new Redis({ host: "localhost", port: 6379 });
const subClient = pubClient.duplicate();
io.adapter(createAdapter(pubClient, subClient));
```

Arranca Redis localmente (`docker run -p 6379:6379 redis`), añade el adapter a `server.js` y ejecuta dos servidores en puertos distintos (`PORT=3000 node server.js` y `PORT=3001 node server.js`): los broadcasts llegarán a los clientes de ambos.
