/**
 * HTTP client connection pooling with keep-alive agents.
 * Uses axios with http.Agent / https.Agent for connection reuse.
 */

const http = require('http');
const https = require('https');
const axios = require('axios');

const httpAgent = new http.Agent({ keepAlive: true, maxSockets: 20 });
const httpsAgent = new https.Agent({ keepAlive: true, maxSockets: 20 });

const api = axios.create({
  httpAgent,
  httpsAgent,
  timeout: 5000,
});

async function fetchData(url) {
  const res = await api.get(url);
  return res.data;
}

function poolStatus() {
  return {
    httpSockets: httpAgent.sockets,
    httpsSockets: httpsAgent.sockets,
    httpFreeSockets: httpAgent.freeSockets,
    httpsFreeSockets: httpsAgent.freeSockets,
  };
}

module.exports = { api, fetchData, poolStatus };

if (require.main === module) {
  fetchData('https://api.example.com/data')
    .then(data => console.log('Data:', data))
    .then(() => console.log('Pool status:', poolStatus()))
    .catch(err => console.error('Error:', err.message));
}