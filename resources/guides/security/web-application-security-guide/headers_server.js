// Zero-dependency Node server that sends the full security header set.
//   node headers_server.js
//   curl -i http://localhost:3000/
const http = require('http');

const HEADERS = {
  'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
  'Content-Security-Policy': "default-src 'self'; frame-ancestors 'none'",
  'X-Frame-Options': 'DENY',
  'X-Content-Type-Options': 'nosniff',
  'Referrer-Policy': 'strict-origin-when-cross-origin',
  'Permissions-Policy': 'camera=(), microphone=(), geolocation=()',
};

const server = http.createServer((req, res) => {
  if (!['GET', 'HEAD'].includes(req.method)) {
    res.writeHead(405, { ...HEADERS, Allow: 'GET, HEAD' }).end('Method Not Allowed');
    return;
  }
  res.writeHead(200, { ...HEADERS, 'Content-Type': 'text/plain' });
  res.end('ok\n');
});

const PORT = process.env.PORT || 3000;

server.listen(PORT, () => {
  console.log(`listening on http://localhost:${PORT} — check the headers with curl -i`);
});
