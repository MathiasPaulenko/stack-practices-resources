// Arrival-rate scenario (open model): drive RPS directly, let k6 scale VUs.
// Watch dropped_iterations — it means the generator can't keep the rate.
// Run: k6 run scenario.js

import http from 'k6/http';
import { check } from 'k6';

const BASE_URL = __ENV.BASE_URL || 'https://api.example.com';

export const options = {
  scenarios: {
    api_traffic: {
      executor: 'ramping-arrival-rate',
      startRate: 50,
      timeUnit: '1s',
      preAllocatedVUs: 100,
      maxVUs: 500,
      stages: [
        { target: 100, duration: '5m' },   // 100 RPS
        { target: 300, duration: '5m' },   // push to 300 RPS
        { target: 0, duration: '2m' },
      ],
    },
  },
  thresholds: {
    http_req_duration: ['p(95)<500'],
    'http_req_duration{endpoint:products}': ['p(95)<300'],
    http_req_failed: [{ threshold: 'rate<0.005', abortOnFail: true, delayAbortEval: '10s' }],
  },
};

export default function () {
  check(
    http.get(`${BASE_URL}/products`, { tags: { endpoint: 'products' } }),
    { 'ok': (r) => r.status === 200 },
  );
}
