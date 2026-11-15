// Smoke test for CI: 1 VU, 1 iteration, strict thresholds. Fast PR gate.
// Run: k6 run --env BASE_URL=... smoke.js

import http from 'k6/http';
import { check } from 'k6';

const BASE_URL = __ENV.BASE_URL || 'https://api.example.com';

export const options = {
  vus: 1,
  iterations: 1,
  thresholds: {
    http_req_duration: ['max<2000'],
    http_req_failed: ['rate===0'],
  },
};

export default function () {
  for (const endpoint of ['/health', '/products', '/users/me']) {
    const res = http.get(`${BASE_URL}${endpoint}`);
    check(res, { [`${endpoint} is 200`]: (r) => r.status === 200 });
  }
}
