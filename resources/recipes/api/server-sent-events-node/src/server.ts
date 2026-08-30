import express, { Request, Response } from 'express';
import { randomUUID } from 'crypto';
import cors from 'cors';
import path from 'path';
import { fileURLToPath } from 'url';

const app = express();
const PORT = 3000;

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

interface Client {
  id: string;
  response: Response;
}

interface SseMessage {
  id: string;
  event: string;
  data: unknown;
  retry?: number;
}

const clients = new Map<string, Client>();
const eventLog: SseMessage[] = [];
const HISTORY_LIMIT = 500;

function formatMessage(msg: SseMessage): string {
  let payload = `id: ${msg.id}\nevent: ${msg.event}\ndata: ${JSON.stringify(msg.data)}\n`;
  if (msg.retry) {
    payload += `retry: ${msg.retry}\n`;
  }
  payload += '\n';
  return payload;
}

function addClient(res: Response): string {
  const id = randomUUID();

  res.writeHead(200, {
    'Content-Type': 'text/event-stream',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'X-Accel-Buffering': 'no',
  });

  const connected: SseMessage = {
    id: randomUUID(),
    event: 'connected',
    data: { clientId: id },
  };

  res.write(formatMessage(connected));
  clients.set(id, { id, response: res });

  res.on('close', () => {
    clients.delete(id);
  });

  res.on('error', () => {
    clients.delete(id);
  });

  return id;
}

function broadcast(msg: SseMessage) {
  eventLog.push(msg);
  if (eventLog.length > HISTORY_LIMIT) {
    eventLog.shift();
  }

  const payload = formatMessage(msg);

  clients.forEach((client) => {
    const flushed = client.response.write(payload);

    if (!flushed) {
      client.response.once('drain', () => {
        // buffer cleared
      });
    }
  });
}

function replayAfter(clientId: string, lastEventId: string) {
  const client = clients.get(clientId);
  if (!client) return;

  const index = eventLog.findIndex((m) => m.id === lastEventId);
  const toReplay = index >= 0 ? eventLog.slice(index + 1) : eventLog;

  toReplay.forEach((msg) => {
    client.response.write(formatMessage(msg));
  });
}

app.use(cors());
app.use(express.static(path.join(__dirname, '..', 'public')));

app.get('/', (_req, res) => {
  res.redirect('/client.html');
});

app.get('/events', (req: Request, res: Response) => {
  const lastEventId = req.headers['last-event-id'] as string | undefined;
  const clientId = addClient(res);

  if (lastEventId) {
    replayAfter(clientId, lastEventId);
  }
});

const server = app.listen(PORT, () => {
  console.log(`SSE server listening on http://localhost:${PORT}`);
});

// Heartbeat every 30 seconds
setInterval(() => {
  broadcast({
    id: randomUUID(),
    event: 'heartbeat',
    data: { ts: Date.now() },
  });
}, 30000);

// Demo notification every 5 seconds
let counter = 0;
setInterval(() => {
  counter += 1;
  broadcast({
    id: randomUUID(),
    event: 'notification',
    data: {
      message: `Server notification #${counter}`,
      ts: Date.now(),
    },
  });
}, 5000);

function shutdown() {
  clients.forEach((client) => {
    client.response.end();
  });
  server.close(() => {
    console.log('Server closed');
    process.exit(0);
  });
}

process.on('SIGTERM', shutdown);
process.on('SIGINT', shutdown);
