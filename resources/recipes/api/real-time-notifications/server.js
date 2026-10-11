// Real-time notification server: WebSocket rooms + Redis pub/sub fan-out.
// Usage: REDIS_URL=redis://localhost:6379 node server.js
const WebSocket = require('ws');
const Redis = require('ioredis');

const REDIS_URL = process.env.REDIS_URL || 'redis://localhost:6379';
const PORT = Number(process.env.PORT || 8080);

const redis = new Redis(REDIS_URL);
const subscriber = new Redis(REDIS_URL);

const wss = new WebSocket.Server({ port: PORT });
const rooms = new Map(); // room name -> Set of connected clients

wss.on('connection', (ws, req) => {
  const room =
    new URL(req.url, `http://localhost:${PORT}`).searchParams.get('room') ||
    'default';
  if (!rooms.has(room)) rooms.set(room, new Set());
  rooms.get(room).add(ws);
  console.log(`client joined room "${room}" (${rooms.get(room).size} clients)`);

  ws.on('close', () => {
    const members = rooms.get(room);
    members.delete(ws);
    if (members.size === 0) rooms.delete(room);
  });
});

subscriber.subscribe('notifications');
subscriber.on('message', (channel, message) => {
  const { room, text } = JSON.parse(message);
  for (const client of rooms.get(room) ?? []) {
    if (client.readyState === WebSocket.OPEN) {
      client.send(text);
    }
  }
});

console.log(`WebSocket server listening on ws://localhost:${PORT}/?room=<name>`);
