const http = require('node:http');

const server = http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/plain' });
  res.end('ok\n');
});

server.listen(3000, () => {
  console.log('listening on :3000');
});
