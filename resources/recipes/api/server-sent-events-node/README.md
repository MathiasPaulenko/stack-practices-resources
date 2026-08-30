# Server-Sent Events with Node.js and Express

This is the runnable companion for the [StackPractices recipe](https://stackpractices.com/recipes/server-sent-events-node/).

It shows a production-ready Express endpoint that:

- Streams events over a long-lived HTTP connection.
- Tracks connected clients and cleans up on disconnect.
- Sends heartbeats to keep the connection alive.
- Supports `Last-Event-ID` reconnection and a bounded event history.
- Handles backpressure by checking the return value of `response.write`.

## Run

```bash
npm install
npm run dev:server
```

Open `http://localhost:3000` to see the client demo.

## Scripts

- `npm run dev:server` — run with `tsx`.
- `npm run build` — compile TypeScript to `dist/`.
- `npm start` — run the compiled server.

## Deploy behind nginx

Make sure `proxy_buffering` is off and timeouts are high enough:

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
