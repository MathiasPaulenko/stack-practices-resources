// Minimal app for the hardened image demo — listens on 8080 as non-root.
const http = require("http");
const fs = require("fs");

// Runtime secrets come from files, never from the image
const dbPassword = (() => {
  const p = process.env.DB_PASSWORD_FILE;
  return p && fs.existsSync(p) ? fs.readFileSync(p, "utf8").trim() : null;
})();

http.createServer((req, res) => {
  if (req.url === "/health") {
    res.writeHead(200, { "content-type": "application/json" });
    res.end(JSON.stringify({ status: "ok", hasDbSecret: !!dbPassword }));
    return;
  }
  res.writeHead(200);
  res.end("hardened app\n");
}).listen(8080, () => console.log("listening on :8080 as uid", process.getuid()));
