// server/chat-io.ts
// Socket.io variant of the same chat: rooms, reconnection, heartbeat, and
// acknowledgments are built in. Requires the socket.io-client package on
// the frontend. See the recipe "Variants" section for the trade-off.
import { Server } from 'socket.io';

const io = new Server(8080);

io.on('connection', (socket) => {
  const { roomId, userId } = socket.handshake.query as Record<string, string>;
  socket.join(roomId);
  io.to(roomId).emit('presence', { users: usersIn(roomId) });

  socket.on('chat', async (content, ack) => {
    const message = { type: 'chat', userId, content, timestamp: Date.now() };
    await saveMessage(roomId, message);
    io.to(roomId).emit('chat', message);
    ack?.({ delivered: true });
  });

  socket.on('typing', (typing) => {
    socket.to(roomId).emit('typing', { userId, typing });
  });
});

// --- Placeholders; wire to your persistence layer. ---
function usersIn(roomId: string): string[] {
  const room = io.sockets.adapter.rooms.get(roomId);
  return room ? Array.from(room).map(id => io.sockets.sockets.get(id)?.handshake.query.userId as string) : [];
}

async function saveMessage(roomId: string, message: object): Promise<void> {
  console.log('persist', roomId, message);
}
