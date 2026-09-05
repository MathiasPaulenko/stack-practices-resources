const express = require("express");
const app = express();

const clients = new Set();

app.get("/events", (req, res) => {
  res.setHeader("Content-Type", "text/event-stream");
  res.setHeader("Cache-Control", "no-cache");
  res.setHeader("Connection", "keep-alive");
  res.setHeader("X-Accel-Buffering", "no");

  let counter = 0;
  const interval = setInterval(() => {
    counter++;
    const data = JSON.stringify({
      id: counter,
      message: `Update ${counter}`,
      timestamp: Date.now(),
    });
    res.write(`id: ${counter}\ndata: ${data}\n\n`);
  }, 2000);

  req.on("close", () => clearInterval(interval));
});

app.get("/broadcast", (req, res) => {
  res.setHeader("Content-Type", "text/event-stream");
  res.setHeader("Cache-Control", "no-cache");
  res.setHeader("Connection", "keep-alive");

  clients.add(res);
  req.on("close", () => clients.delete(res));
});

app.get("/publish/:message", (req, res) => {
  const message = `data: ${JSON.stringify({ msg: req.params.message })}\n\n`;
  clients.forEach((client) => client.write(message));
  res.json({ published: clients.size });
});

app.listen(3000, () => console.log("SSE server on http://localhost:3000"));
