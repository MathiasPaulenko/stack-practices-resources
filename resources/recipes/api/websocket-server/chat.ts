// server/chat.ts
// WebSocket chat server with rooms, presence, heartbeat, and Redis fan-out.
// Companion file for https://stackpractices.com/recipes/websocket-bidirectional-chat/
import { WebSocketServer, WebSocket, type RawData } from 'ws';
import { createClient } from 'redis';
import { handleTyping } from './typing.js';

interface ChatClient extends WebSocket {
  userId: string;
  roomId: string;
  isAlive: boolean;
}

const wss = new WebSocketServer({ port: 8080 });
export const redis = createClient({ url: 'redis://localhost:6379' });
await redis.connect();

const rooms = new Map<string, Set<ChatClient>>();

wss.on('connection', (ws: ChatClient, req) => {
  const url = new URL(req.url ?? '/', 'http://localhost');
  ws.userId = url.searchParams.get('userId') ?? 'anonymous';
  ws.roomId = url.searchParams.get('roomId') ?? 'lobby';
  ws.isAlive = true;

  ws.on('pong', () => { ws.isAlive = true; });
  joinRoom(ws);
  broadcastPresence(ws.roomId);

  ws.on('message', (data: RawData) => handleMessage(ws, data));
  ws.on('close', () => leaveRoom(ws));
});

// Drop sockets that stop answering pings; stale connections leak rooms.
setInterval(() => {
  wss.clients.forEach((ws) => {
    const client = ws as ChatClient;
    if (!client.isAlive) return client.terminate();
    client.isAlive = false;
    client.ping();
  });
}, 30_000);

function joinRoom(client: ChatClient) {
  if (!rooms.has(client.roomId)) {
    rooms.set(client.roomId, new Set());
  }
  rooms.get(client.roomId)!.add(client);

  client.send(JSON.stringify({
    type: 'system',
    content: `Joined room ${client.roomId}`,
  }));
}

function leaveRoom(client: ChatClient) {
  rooms.get(client.roomId)?.delete(client);
  broadcastPresence(client.roomId);
}

function broadcastPresence(roomId: string) {
  broadcastToRoom(roomId, {
    type: 'presence',
    users: Array.from(rooms.get(roomId) ?? []).map(c => c.userId),
  });
}

async function handleMessage(client: ChatClient, data: RawData) {
  let payload: { type?: string; content?: string; typing?: boolean };
  try {
    payload = JSON.parse(data.toString());
  } catch {
    return; // a malformed frame should not crash the process
  }

  switch (payload.type) {
    case 'chat': {
      const message = {
        type: 'chat',
        userId: client.userId,
        content: String(payload.content ?? '').slice(0, 2000),
        timestamp: Date.now(),
        id: generateId(),
      };

      await saveMessage(client.roomId, message);
      // Every instance, including this one, broadcasts on receipt.
      await redis.publish(
        'chat:messages',
        JSON.stringify({ roomId: client.roomId, message })
      );
      break;
    }
    case 'typing':
      handleTyping(client, Boolean(payload.typing));
      break;
  }
}

export function broadcastToRoom(roomId: string, message: object) {
  const clients = rooms.get(roomId);
  if (!clients) return;

  const data = JSON.stringify(message);
  clients.forEach(client => {
    if (client.readyState === WebSocket.OPEN) {
      client.send(data);
    }
  });
}

// --- Placeholder implementations; wire to your persistence/id layer. ---
function generateId(): string {
  return crypto.randomUUID();
}

async function saveMessage(roomId: string, message: object): Promise<void> {
  // Insert into your messages table/collection here.
  console.log('persist', roomId, message);
}
