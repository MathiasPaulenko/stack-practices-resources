// hooks/useChat.ts
// React client with presence, typed messages, and exponential-backoff
// reconnection that stops when the component unmounts intentionally.
import { useEffect, useRef, useState, useCallback } from 'react';

const WS_URL = 'wss://chat.example.com';
const MAX_BACKOFF_MS = 30_000;

interface ChatMessage {
  type: 'chat' | 'presence' | 'typing' | 'system';
  userId?: string;
  users?: string[];
  content?: string;
  timestamp?: number;
  id?: string;
}

export function useChat(roomId: string, userId: string) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [users, setUsers] = useState<string[]>([]);
  const [connected, setConnected] = useState(false);
  const ws = useRef<WebSocket | null>(null);
  const retries = useRef(0);
  const reconnectTimer = useRef<ReturnType<typeof setTimeout>>();
  const closedByUser = useRef(false);

  const connect = useCallback(() => {
    const socket = new WebSocket(`${WS_URL}?roomId=${roomId}&userId=${userId}`);

    socket.onopen = () => {
      retries.current = 0;
      setConnected(true);
    };

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);

      switch (data.type) {
        case 'chat':
          setMessages(prev => [...prev, data]);
          break;
        case 'presence':
          setUsers(data.users);
          break;
      }
    };

    socket.onclose = () => {
      setConnected(false);
      if (closedByUser.current) return;
      // Exponential backoff: 1s, 2s, 4s... capped at 30s
      const delay = Math.min(MAX_BACKOFF_MS, 1000 * 2 ** retries.current++);
      reconnectTimer.current = setTimeout(connect, delay);
    };

    ws.current = socket;
  }, [roomId, userId]);

  useEffect(() => {
    closedByUser.current = false;
    connect();
    return () => {
      closedByUser.current = true;
      clearTimeout(reconnectTimer.current);
      ws.current?.close();
    };
  }, [connect]);

  const sendMessage = useCallback((content: string) => {
    ws.current?.send(JSON.stringify({ type: 'chat', content }));
  }, []);

  const sendTyping = useCallback((typing: boolean) => {
    ws.current?.send(JSON.stringify({ type: 'typing', typing }));
  }, []);

  return { messages, users, connected, sendMessage, sendTyping };
}
