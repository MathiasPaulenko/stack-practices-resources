const http = require("http");

const server = http.createServer((req, res) => {
    if (req.url === "/health" && req.method === "GET") {
        res.writeHead(200, { "Content-Type": "application/json" });
        res.end(JSON.stringify({ status: "healthy" }));
        return;
    }
    res.writeHead(200, { "Content-Type": "text/plain" });
    res.end("ok");
});

server.listen(3000, () => {
    console.log("listening on :3000");
});
