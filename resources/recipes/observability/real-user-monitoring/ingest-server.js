import http from 'node:http';

// Minimal RUM ingest endpoint: accepts beacon POSTs and logs metrics as JSONL.
// Real deployments push to a metrics pipeline (BigQuery, ClickHouse, Prometheus).

const server = http.createServer((req, res) => {
  if (req.method === 'POST' && req.url === '/analytics/vitals') {
    let body = '';
    req.on('data', (chunk) => (body += chunk));
    req.on('end', () => {
      try {
        const metric = JSON.parse(body);
        console.log(
          `${metric.page}\t${metric.name}=${metric.value} (${metric.rating})`
        );
      } catch {
        console.log('malformed beacon:', body.slice(0, 100));
      }
      res.writeHead(204);
      res.end();
    });
  } else {
    res.writeHead(404);
    res.end();
  }
});

server.listen(8899, () => console.log('RUM ingest on http://localhost:8899'));
