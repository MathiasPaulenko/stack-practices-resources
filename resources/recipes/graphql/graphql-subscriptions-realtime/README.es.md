# Suscripciones GraphQL sobre WebSockets — Companion

Versión ejecutable de la receta: un solo proceso Node sirve GraphQL por HTTP **y** suscripciones por WebSocket en el mismo puerto, con un `PubSub` en memoria detrás.

## Archivos

- `schema.mjs` — typeDefs con las suscripciones `postCreated` / `postUpdated(id)`
- `resolvers.mjs` — cableado de PubSub, filtrado por suscriptor con `withFilter`, publicadores `createPost` / `updatePost`
- `server.mjs` — Express + `expressMiddleware` sobre el mismo `http.Server` al que se engancha `graphql-ws`, con plugins de drenaje
- `demo.mjs` — prueba end-to-end: cliente WS real se suscribe, mutaciones HTTP disparan los eventos
- `tests/subscriptions.test.js` — tests vitest de publicación y filtrado

## Ejecutar

```bash
npm install
npm run demo   # levanta el servidor, se suscribe por WS, dispara mutaciones por HTTP
npm test       # tests vitest
npm start      # servidor standalone en :4000
```

## Qué demuestra

- `asyncIterator` solo acepta topics string; los payloads se publican como `{ [nombreDelCampo]: valor }`
- `withFilter` filtra por suscriptor (`postUpdated(id:)` solo dispara para el id pedido)
- HTTP y WS comparten puerto; los plugins de drenaje cierran los sockets limpiamente al apagar
