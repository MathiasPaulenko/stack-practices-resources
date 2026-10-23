// server/redis-broadcast.ts
// Subscribes every server instance to the shared channel and relays
// messages to local rooms. The publisher receives its own message through
// pub/sub, so there is a single broadcast path (no local/remote duplication).
import { redis, broadcastToRoom } from './chat.js';

const subscriber = redis.duplicate();
await subscriber.connect();

// node-redis v4: subscribe(channel, (message, channel) => void)
await subscriber.subscribe('chat:messages', (raw) => {
  const { roomId, message } = JSON.parse(raw);
  broadcastToRoom(roomId, message);
});
