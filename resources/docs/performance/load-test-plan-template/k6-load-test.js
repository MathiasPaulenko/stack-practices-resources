import http from 'k6/http';
import { check, sleep, group } from 'k6';
import { Rate, Trend } from 'k6/metrics';

const errorRate = new Rate('errors');
const responseTime = new Trend('response_time');

export const options = {
  stages: [
    { duration: '2m', target: 10 },   // warmup
    { duration: '10m', target: 50 },  // baseline
    { duration: '5m', target: 200 },  // ramp-up
    { duration: '15m', target: 200 }, // peak hold
    { duration: '2m', target: 0 },    // ramp-down
  ],
  thresholds: {
    http_req_duration: ['p(95)<300', 'p(99)<500'],
    http_req_failed: ['rate<0.01'],
    errors: ['rate<0.001'],
  },
};

const BASE_URL = 'https://staging.example.com';

export default function () {
  // Journey: Browse homepage
  group('Browse homepage', function () {
    const homeRes = http.get(`${BASE_URL}/`);
    check(homeRes, {
      'homepage status 200': (r) => r.status === 200,
      'homepage LCP < 2.5s': (r) => r.timings.waiting < 2500,
    });
    errorRate.add(homeRes.status !== 200);
    responseTime.add(homeRes.timings.duration);
    sleep(1);
  });

  // Journey: View product
  group('View product', function () {
    const productId = Math.floor(Math.random() * 10000) + 1;
    const productRes = http.get(`${BASE_URL}/api/products/${productId}`);
    check(productRes, {
      'product status 200': (r) => r.status === 200,
      'product has name': (r) => r.json('name') !== undefined,
    });
    errorRate.add(productRes.status !== 200);
    responseTime.add(productRes.timings.duration);
    sleep(2);
  });

  // Journey: Search
  group('Search', function () {
    const queries = ['laptop', 'phone', 'headphones', 'keyboard', 'mouse'];
    const query = queries[Math.floor(Math.random() * queries.length)];
    const searchRes = http.get(`${BASE_URL}/api/search?q=${query}`);
    check(searchRes, {
      'search status 200': (r) => r.status === 200,
      'search returns results': (r) => r.json('results').length > 0,
    });
    errorRate.add(searchRes.status !== 200);
    responseTime.add(searchRes.timings.duration);
    sleep(1.5);
  });
}
