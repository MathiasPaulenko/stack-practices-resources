// Baseline API load test: staged ramp + pass/fail thresholds.
// Run: k6 run k6-load-test.js
import http from 'k6/http';
import { check, sleep } from 'k6';

const BASE_URL = __ENV.BASE_URL || 'https://api.example.com';

export const options = {
  stages: [
    { duration: '2m', target: 100 },   // ramp up to 100 users
    { duration: '5m', target: 100 },   // sustain load
    { duration: '2m', target: 200 },   // ramp up to 200 users
    { duration: '5m', target: 200 },   // sustain higher load
    { duration: '2m', target: 0 },     // ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],   // 95% of requests under 500ms
    http_req_failed: ['rate<0.01'],     // error rate below 1%
  },
};

export default function () {
  const res = http.get(`${BASE_URL}/users`);
  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });
  sleep(1);
}
