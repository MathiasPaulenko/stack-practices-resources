const http = require('http');

const server = http.createServer((req, res) => {
  if (req.url === '/health') {
    res.writeHead(200);
    return res.end('ok');
  }
  res.writeHead(200);
  res.end('hello from distroless node\n');
});

server.listen(3000, () => console.log('listening on :3000'));
