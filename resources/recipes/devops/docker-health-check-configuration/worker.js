// worker.js — Writes a heartbeat file the Dockerfile health check
// measures for staleness, since this process has no HTTP listener.
const fs = require("fs");

setInterval(() => {
    fs.writeFileSync("/tmp/worker.heartbeat", new Date().toISOString());
}, 30000);

setInterval(() => {
    // Process queue messages here.
    console.log("worker tick", new Date().toISOString());
}, 60000);
