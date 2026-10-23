// server/typing.ts
// Per-room typing indicator state. handleTyping is invoked from the
// message dispatcher in chat.ts when a {type: 'typing'} frame arrives.
import type { WebSocket } from 'ws';
import { broadcastToRoom } from './chat.js';

interface ChatClient extends WebSocket {
  userId: string;
  roomId: string;
}

const typingUsers = new Map<string, Set<string>>();

export function handleTyping(client: ChatClient, isTyping: boolean) {
  if (!typingUsers.has(client.roomId)) {
    typingUsers.set(client.roomId, new Set());
  }

  const room = typingUsers.get(client.roomId)!;
  if (isTyping) room.add(client.userId);
  else room.delete(client.userId);

  broadcastToRoom(client.roomId, {
    type: 'typing',
    users: Array.from(room),
  });
}
