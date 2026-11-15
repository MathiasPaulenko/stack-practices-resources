// Basic load test: staged ramp, SLO thresholds, checks.
// Run: k6 run basic.js

import http from 'k6/http';
import { check, sleep } from 'k6';

const BASE_URL = __ENV.BASE_URL || 'https://api.example.com';

export const options = {
  stages: [
    { duration: '2m', target: 100 },   // ramp up
    { duration: '5m', target: 100 },   // steady state
    { duration: '2m', target: 200 },   // spike
    { duration: '5m', target: 200 },   // sustained load
    { duration: '2m', target: 0 },     // ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500', 'p(99)<1000'],
    http_req_failed: [{ threshold: 'rate<0.005', abortOnFail: true, delayAbortEval: '10s' }],
  },
};

export default function () {
  const res = http.get(`${BASE_URL}/products`);

  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
    'has products array': (r) => Array.isArray(r.json()) && r.json().length > 0,
  });

  sleep(1);
}
