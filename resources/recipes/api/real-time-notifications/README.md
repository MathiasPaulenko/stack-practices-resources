# Real-Time Notifications with WebSockets — Companion Resources

Companion files for [Build Real-Time Notifications with WebSockets](https://stackpractices.com/recipes/real-time-notifications/) on StackPractices.

## Files

| File | What it demonstrates |
|------|----------------------|
| `server.js` | WebSocket server with room-based routing and Redis pub/sub fan-out across instances |
| `client.html` | Browser client that joins a room, renders notifications, and reconnects with exponential backoff |
| `publish.js` | CLI that publishes a `{room, text}` message to the `notifications` channel |
| `package.json` | Dependencies (`ws`, `ioredis`) and start scripts |
| `docker-compose.yml` | Single-service Redis 7 for local testing |

## How to use

```bash
docker compose up -d        # start Redis
npm install                 # install ws + ioredis
npm start                   # start the WebSocket server on :8080
```

Open `client.html` in a browser (optionally with `?room=orders` in the URL), then from another terminal:

```bash
node publish.js orders "New order!"   # push a notification to the room
```

To see multi-instance fan-out, run `PORT=8081 node server.js` next to the default instance — a publish reaches clients on both.

No dependencies beyond Node.js ≥ 18, Docker, and the two npm packages.
