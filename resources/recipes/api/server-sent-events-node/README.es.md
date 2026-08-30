# Server-Sent Events con Node.js y Express

Companion ejecutable para la [receta de StackPractices](https://stackpractices.com/recipes/server-sent-events-node/).

Muestra un endpoint de Express listo para producción que:

- Hace stream de eventos sobre una conexión HTTP persistente.
- Rastrea clientes conectados y limpia al desconectarse.
- Envía heartbeats para mantener la conexión viva.
- Soporta reconexión con `Last-Event-ID` y un historial acotado.
- Maneja backpressure revisando lo que devuelve `response.write`.

## Ejecutar

```bash
npm install
npm run dev:server
```

Abrí `http://localhost:3000` para ver la demo del cliente.

## Scripts

- `npm run dev:server` — corre con `tsx`.
- `npm run build` — compila TypeScript a `dist/`.
- `npm start` — corre el servidor compilado.

## Desplegar detrás de nginx

Asegurate de que `proxy_buffering` esté desactivado y los timeouts sean
suficientemente altos:

```nginx
location /events {
  proxy_pass http://localhost:3000;
  proxy_http_version 1.1;
  proxy_set_header Connection '';
  proxy_buffering off;
  proxy_cache off;
  proxy_read_timeout 86400s;
  proxy_send_timeout 86400s;
}
```
