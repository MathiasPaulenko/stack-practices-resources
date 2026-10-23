# Chat con WebSocket — Recursos Complementarios

Proyecto companion de la [receta de servidor WebSocket](https://stackpractices.com/es/recipes/websocket-server/) en StackPractices: una aplicación de chat bidireccional completa construida sobre ella (ver la sección "Construyendo una aplicación de chat").

## Contenido

- `chat.ts` — servidor `ws` con gestión de salas, difusión de presencia, heartbeat ping/pong de 30 segundos, manejo de payloads malformados y fan-out de mensajes por Redis pub/sub.
- `redis-broadcast.ts` — suscripción que reenvía los mensajes publicados a las salas locales de cada instancia (ruta de difusión única, sin duplicación local/remota).
- `typing.ts` — estado de indicadores de escritura por sala, conectado al dispatcher de mensajes.
- `useChat.ts` — hook de React que expone `messages`, `users`, `connected`, `sendMessage` y `sendTyping`, con reconexión de backoff exponencial limitada a 30 s.
- `chat-io.ts` — variante con Socket.io del mismo chat (salas, heartbeat y acuses de recibo incluidos).
- `package.json` — dependencias y scripts de arranque.

## Uso

```bash
npm install
npm start        # servidor ws en :8080 (requiere Redis en localhost:6379)
npm run start:io # variante Socket.io en :8080
```

Después apunta `useChat(roomId, userId)` de tu app React a `wss://tu-host?roomId=...&userId=...`.

`saveMessage` y `generateId` son implementaciones placeholder en `chat.ts`; conéctalos a tu capa de persistencia.
