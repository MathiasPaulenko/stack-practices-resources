// Demo app: emits structured JSON logs to stdout for Fluentd's parser filter.
const http = require("http");

const logger = {
    info(message, meta = {}) {
        console.log(JSON.stringify({
            level: "info",
            message,
            timestamp: new Date().toISOString(),
            service: "api",
            ...meta
        }));
    },
    error(message, meta = {}) {
        console.error(JSON.stringify({
            level: "error",
            message,
            timestamp: new Date().toISOString(),
            service: "api",
            ...meta
        }));
    }
};

const server = http.createServer((req, res) => {
    const start = Date.now();
    if (req.url === "/fail") {
        logger.error("Request failed", { method: req.method, path: req.url });
        res.writeHead(500, { "Content-Type": "application/json" });
        res.end(JSON.stringify({ error: "boom" }));
        return;
    }
    res.writeHead(200, { "Content-Type": "application/json" });
    res.end(JSON.stringify({ ok: true }));
    logger.info("Request received", {
        method: req.method,
        path: req.url,
        duration: Date.now() - start
    });
});

server.listen(3000, () => logger.info("Server listening", { port: 3000 }));
