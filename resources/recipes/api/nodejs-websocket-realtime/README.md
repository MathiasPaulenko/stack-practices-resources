# Socket.io Real-Time Chat — Companion Project

Runnable companion to the StackPractices recipe [Node.js WebSocket Real-Time Communication with Socket.io](https://stackpractices.com/recipes/nodejs-websocket-realtime/).

## What's inside

- `server.js` — Express + Socket.io chat server: user registry, rooms (`join-room`/`leave-room`/`room-message`), broadcasting, typing indicators, presence cleanup on `disconnect`.
- `client.js` — Node-based Socket.io client that joins, sends messages every 5s, and prints chat traffic. Run two instances to see real-time delivery.

## Run it

```bash
npm install
npm start          # server on :3000

# in another terminal
npm run client     # or: USERNAME=bob node client.js
# and another
USERNAME=alice node client.js
```

## Optional: Redis adapter for multi-instance scaling

The `package.json` includes `@socket.io/redis-adapter` and `ioredis` as optional dependencies. To scale across instances:

```javascript
import { createAdapter } from "@socket.io/redis-adapter";
import { Redis } from "ioredis";

const pubClient = new Redis({ host: "localhost", port: 6379 });
const subClient = pubClient.duplicate();
io.adapter(createAdapter(pubClient, subClient));
```

Start Redis locally (`docker run -p 6379:6379 redis`), add the adapter to `server.js`, then run two servers on different ports (`PORT=3000 node server.js` and `PORT=3001 node server.js`) — broadcasts will reach clients on both.
