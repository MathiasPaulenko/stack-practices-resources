# GraphQL Subscriptions over WebSockets — Companion

Runnable version of the recipe: one Node process serves GraphQL over HTTP **and** subscriptions over WebSocket on the same port, backed by an in-memory `PubSub`.

## Files

- `schema.mjs` — typeDefs with `postCreated` / `postUpdated(id)` subscriptions
- `resolvers.mjs` — PubSub wiring, `withFilter` per-subscriber filtering, `createPost` / `updatePost` publishers
- `server.mjs` — Express + `expressMiddleware` on the same `http.Server` the `graphql-ws` server attaches to, with drain plugins
- `demo.mjs` — end-to-end proof: real WS client subscribes, HTTP mutations trigger the events
- `tests/subscriptions.test.js` — vitest unit tests for publish/filter behavior

## Run

```bash
npm install
npm run demo   # starts the server, subscribes over WS, fires mutations over HTTP
npm test       # vitest unit tests
npm start      # standalone server on :4000
```

## What it demonstrates

- `asyncIterator` takes topic strings only; payloads publish as `{ [fieldName]: value }`
- `withFilter` filters per subscriber (`postUpdated(id:)` only fires for the requested id)
- HTTP and WS share the port; the drain plugins close sockets cleanly on shutdown
