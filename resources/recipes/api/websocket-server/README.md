# WebSocket Chat — Companion Resources

Companion project for the [WebSocket server recipe](https://stackpractices.com/recipes/websocket-server/) on StackPractices — a complete bidirectional chat application built on top of it (see the "Building a Chat Application" section).

## Contents

- `chat.ts` — `ws` server with room management, presence broadcast, a 30-second ping/pong heartbeat, malformed-payload handling, and message fan-out through Redis pub/sub.
- `redis-broadcast.ts` — subscription that relays published messages to local rooms on every server instance (single broadcast path, no local/remote duplication).
- `typing.ts` — per-room typing indicator state, wired into the message dispatcher.
- `useChat.ts` — React hook exposing `messages`, `users`, `connected`, `sendMessage`, and `sendTyping`, with exponential-backoff reconnection capped at 30 s.
- `chat-io.ts` — Socket.io variant of the same chat (rooms, heartbeat, and acknowledgments built in).
- `package.json` — dependencies and start scripts.

## Usage

```bash
npm install
npm start        # ws server on :8080 (needs Redis on localhost:6379)
npm run start:io # Socket.io variant on :8080
```

Then point `useChat(roomId, userId)` in your React app at `wss://your-host?roomId=...&userId=...`.

`saveMessage` and `generateId` are placeholder implementations in `chat.ts`; wire them to your persistence layer.
