// shutdown/graceful.js — Graceful shutdown for Node.js Express
const express = require("express");
const http = require("http");

const app = express();
const server = http.createServer(app);

let isShuttingDown = false;
let activeRequests = 0;

// Track active requests
app.use((req, res, next) => {
    if (isShuttingDown) {
        res.setHeader("Connection", "close");
        return res.status(503).json({ error: "Server shutting down" });
    }
    activeRequests++;
    res.on("finish", () => activeRequests--);
    next();
});

app.get("/health", (req, res) => {
    if (isShuttingDown) {
        return res.status(503).json({ status: "shutting_down" });
    }
    res.json({ status: "healthy" });
});

app.get("/api/data", (req, res) => {
    setTimeout(() => {
        res.json({ data: "response", activeRequests });
    }, 500);
});

// Graceful shutdown
function gracefulShutdown(signal) {
    console.log(`Received ${signal}, starting graceful shutdown...`);
    isShuttingDown = true;

    // Stop accepting new connections
    server.close(() => {
        console.log("HTTP server closed");
    });

    // Wait for active requests
    const checkInterval = setInterval(() => {
        if (activeRequests === 0) {
            clearInterval(checkInterval);
            console.log("All requests completed, exiting");
            cleanup();
        }
    }, 100);

    // Force exit after timeout
    setTimeout(() => {
        console.log(`Timeout: ${activeRequests} requests still active, forcing exit`);
        cleanup();
    }, 30000);
}

function cleanup() {
    // Close database connections
    // Flush log buffers
    // Close message queue connections
    console.log("Cleanup complete, exiting");
    process.exit(0);
}

process.on("SIGTERM", () => gracefulShutdown("SIGTERM"));
process.on("SIGINT", () => gracefulShutdown("SIGINT"));

server.listen(8080, () => console.log("Server running on port 8080"));
