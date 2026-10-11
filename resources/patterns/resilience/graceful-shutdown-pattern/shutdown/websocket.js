// shutdown/websocket.js — Graceful shutdown for WebSocket server
const { WebSocketServer } = require("ws");

const wss = new WebSocketServer({ port: 8080 });
let isShuttingDown = false;

wss.on("connection", (ws) => {
    if (isShuttingDown) {
        ws.close(1001, "Server shutting down");
        return;
    }

    ws.on("message", (data) => {
        ws.send(`Echo: ${data}`);
    });
});

function gracefulShutdown() {
    console.log("WebSocket graceful shutdown...");
    isShuttingDown = true;

    // Close all connections with "going away" code
    wss.clients.forEach((ws) => {
        ws.close(1001, "Server shutting down");
    });

    // Close server after all clients disconnect
    setTimeout(() => {
        wss.close(() => {
            console.log("WebSocket server closed");
            process.exit(0);
        });
    }, 5000);
}

process.on("SIGTERM", gracefulShutdown);
