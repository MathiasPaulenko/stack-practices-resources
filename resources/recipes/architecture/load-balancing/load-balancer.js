/**
 * Least-response-time balancer demo.
 *
 * Picks the healthy backend with the lowest score: rolling average latency
 * plus a 10% penalty per in-flight connection, so a degraded server sheds
 * traffic before it fails outright. Run: node load-balancer.js
 */

class LeastResponseTimeBalancer {
  constructor() {
    this.servers = [];
    this.responseTimes = new Map();
  }

  addServer(url) {
    this.servers.push({
      url,
      activeConnections: 0,
      avgResponseTime: 0,
      lastResponseAt: Date.now(),
      healthy: true,
    });
    this.responseTimes.set(url, []);
  }

  selectServer() {
    const healthy = this.servers.filter((s) => s.healthy);
    if (healthy.length === 0) return null;
    let best = healthy[0];
    for (const server of healthy) {
      if (this.score(server) < this.score(best)) best = server;
    }
    best.activeConnections++;
    return best;
  }

  score(server) {
    return server.avgResponseTime * (1 + server.activeConnections / 10);
  }

  recordResponse(url, responseTimeMs) {
    const times = this.responseTimes.get(url) || [];
    times.push(responseTimeMs);
    if (times.length > 100) times.shift();

    const server = this.servers.find((s) => s.url === url);
    if (server) {
      server.avgResponseTime = times.reduce((a, b) => a + b, 0) / times.length;
      server.activeConnections = Math.max(0, server.activeConnections - 1);
      server.lastResponseAt = Date.now();
    }
    this.responseTimes.set(url, times);
  }

  markUnhealthy(url) {
    const server = this.servers.find((s) => s.url === url);
    if (server) server.healthy = false;
  }
}

// Fake backends with different latency profiles
const LATENCIES = { 'api-1': 20, 'api-2': 50, 'api-3': 120 };

const balancer = new LeastResponseTimeBalancer();
for (const url of Object.keys(LATENCIES)) balancer.addServer(url);

console.log('== Least response time (3 backends, different latencies) ==');
const picks = {};
for (let i = 0; i < 30; i++) {
  const server = balancer.selectServer();
  picks[server.url] = (picks[server.url] || 0) + 1;
  // simulate a response so connections drain
  balancer.recordResponse(server.url, LATENCIES[server.url] + (Math.random() * 10 - 5));
}
console.log('picks:', picks, '(fastest backend should win most)');

console.log('\n== api-1 marked unhealthy ==');
balancer.markUnhealthy('api-1');
const picks2 = {};
for (let i = 0; i < 10; i++) {
  const server = balancer.selectServer();
  picks2[server.url] = (picks2[server.url] || 0) + 1;
  balancer.recordResponse(server.url, LATENCIES[server.url]);
}
console.log('picks:', picks2, '(api-1 must get zero)');
