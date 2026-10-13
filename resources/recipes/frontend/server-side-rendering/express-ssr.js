// Minimal SSR by hand: Express + ReactDOMServer.
// Educational — shows what frameworks abstract away.
// Production needs streaming (renderToPipeableStream), code splitting, and asset handling.

// server.js
import express from 'express';
import React from 'react';
import { renderToString } from 'react-dom/server';
import { App } from './App.js';

const app = express();
app.use(express.static('public')); // serves /client.js (the hydration bundle)

app.get('*', (req, res) => {
  // Render the same component tree the client will hydrate
  const html = renderToString(<App url={req.url} />);

  res.send(`<!doctype html>
    <html>
      <head><title>SSR Example</title></head>
      <body>
        <div id="root">${html}</div>
        <script src="/client.js"></script>
      </body>
    </html>`);
});

app.listen(3000, () => console.log('SSR on :3000'));

// client.js — the hydration bundle (built with your bundler of choice):
// import { hydrateRoot } from 'react-dom/client';
// import { App } from './App.js';
// hydrateRoot(document.getElementById('root'), <App url={window.location.pathname} />);
//
// The url prop MUST match between server render and client hydration,
// or you get a hydration mismatch: React discards the server DOM and re-renders.
