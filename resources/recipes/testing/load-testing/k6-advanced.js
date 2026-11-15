// Advanced load test: token reuse via setup(), SharedArray CSV data,
// weighted scenarios, and an abortOnFail threshold for production-adjacent runs.
// Run: BASE_URL=https://api.example.com CLIENT_SECRET=xxx k6 run k6-advanced.js
import http from 'k6/http';
import { check, sleep } from 'k6';
import { SharedArray } from 'k6/data';
import papaparse from 'https://jslib.k6.io/papaparse/5.1.1/index.js';

const BASE_URL = __ENV.BASE_URL || 'https://api.example.com';

const users = new SharedArray('users', () =>
  papaparse.parse(open('./users.csv'), { header: true }).data
);

export const options = {
  scenarios: {
    browsing: {
      executor: 'ramping-vus',
      stages: [{ duration: '5m', target: 80 }],
      exec: 'browse',
    },
    shopping: {
      executor: 'ramping-vus',
      stages: [{ duration: '5m', target: 15 }],
      exec: 'shop',
    },
    checkout: {
      executor: 'ramping-vus',
      stages: [{ duration: '5m', target: 5 }],
      exec: 'checkout',
    },
  },
  thresholds: {
    http_req_duration: ['p(95)<500'],
    http_req_failed: [
      { threshold: 'rate<0.01' },
      // Hard abort if errors spike — protects the target during
      // production-adjacent runs.
      { threshold: 'rate<0.05', abortOnFail: true, delayAbortEval: '30s' },
    ],
  },
};

// Log in once per test, not once per VU.
export function setup() {
  const res = http.post(`${BASE_URL}/oauth/token`, {
    client_id: 'test_client',
    client_secret: __ENV.CLIENT_SECRET,
    grant_type: 'client_credentials',
  });
  return { token: res.json('access_token') };
}

function authHeaders(token) {
  return { headers: { Authorization: `Bearer ${token}` } };
}

export function browse(data) {
  const res = http.get(`${BASE_URL}/products`, authHeaders(data.token));
  check(res, { 'browse ok': (r) => r.status === 200 });
  sleep(5 + Math.random() * 25);
}

export function shop(data) {
  const user = users[__VU % users.length];
  http.get(`${BASE_URL}/products`, authHeaders(data.token));
  const res = http.post(
    `${BASE_URL}/cart`,
    JSON.stringify({ productId: 1, user: user.email }),
    { headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${data.token}` } }
  );
  check(res, { 'cart ok': (r) => r.status === 200 || r.status === 201 });
  sleep(10 + Math.random() * 50);
}

export function checkout(data) {
  const res = http.post(
    `${BASE_URL}/cart/checkout`,
    JSON.stringify({ paymentMethod: 'card' }),
    { headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${data.token}` } }
  );
  check(res, { 'checkout ok': (r) => r.status === 200 });
  sleep(30 + Math.random() * 90);
}
