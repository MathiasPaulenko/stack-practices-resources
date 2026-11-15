// CSV-driven test data with SharedArray (parsed once, shared by all VUs).
// Requires users.csv in the same directory.
// Run: k6 run data.js

import http from 'k6/http';
import { check } from 'k6';
import { SharedArray } from 'k6/data';

const BASE_URL = __ENV.BASE_URL || 'https://api.example.com';

const users = new SharedArray('users', () =>
  open('./users.csv')
    .split('\n')
    .slice(1)
    .filter(Boolean)
    .map((line) => {
      const [email, password] = line.split(',');
      return { email, password };
    }),
);

export const options = { vus: 20, duration: '2m' };

export default function () {
  const user = users[__VU % users.length];
  check(http.post(`${BASE_URL}/login`, JSON.stringify(user)), {
    'login ok': (r) => r.status === 200,
  });
}
