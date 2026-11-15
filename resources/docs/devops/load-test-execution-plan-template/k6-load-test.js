// k6 load test script matching the execution-plan template.
// Ramps to the peak scenario VU count, tags requests with a correlation ID,
// and records a custom failure rate as a Rate metric for thresholds.
// Run: k6 run k6-load-test.js
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate } from 'k6/metrics';

const failureRate = new Rate('check_failure_rate');

export const options = {
  stages: [
    { duration: '2m', target: 100 },
    { duration: '5m', target: 100 },
    { duration: '2m', target: 300 },
    { duration: '5m', target: 300 },
    { duration: '2m', target: 500 },
    { duration: '5m', target: 500 },
    { duration: '2m', target: 2000 },
    { duration: '5m', target: 2000 },
    { duration: '5m', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(95)<500', 'p(99)<1000'],
    http_req_failed: ['rate<0.01'],
    check_failure_rate: ['rate<0.05'],
  },
};

export default function () {
  const headers = {
    'X-Correlation-Id': `corr_${__VU}_${__ITER}`,
    'Content-Type': 'application/json',
  };

  const loginRes = http.post('https://api.example.com/auth/login', JSON.stringify({
    username: `user_${__VU % 100}`,
    password: 'test-password',
  }), { headers });

  const loginOk = check(loginRes, {
    'login status 200': (r) => r.status === 200,
    'login has token': (r) => r.json('token') !== undefined,
  });
  failureRate.add(!loginOk);

  sleep(Math.random() * 2 + 1);

  const listRes = http.get('https://api.example.com/orders', {
    headers: { ...headers, Authorization: `Bearer ${loginRes.json('token')}` },
  });

  const ordersOk = check(listRes, {
    'orders status 200': (r) => r.status === 200,
    'orders has items': (r) => r.json('items').length > 0,
  });
  failureRate.add(!ordersOk);

  sleep(Math.random() * 3 + 1);
}
