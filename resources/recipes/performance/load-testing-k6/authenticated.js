// Authenticated workflow: token via setup(), cart -> checkout flow.
// Run: k6 run --env BASE_URL=... --env CLIENT_ID=... --env CLIENT_SECRET=... authenticated.js

import http from 'k6/http';
import { check } from 'k6';

const BASE_URL = __ENV.BASE_URL || 'https://api.example.com';

export function setup() {
  const res = http.post(`${BASE_URL}/oauth/token`, {
    client_id: __ENV.CLIENT_ID,
    client_secret: __ENV.CLIENT_SECRET,
    grant_type: 'client_credentials',
  });
  return { token: res.json('access_token') };
}

export const options = { vus: 50, duration: '10m' };

export default function (data) {
  const params = {
    headers: {
      Authorization: `Bearer ${data.token}`,
      'Content-Type': 'application/json',
    },
  };

  const cart = http.post(`${BASE_URL}/cart`, JSON.stringify({ items: [1, 2, 3] }), params);
  check(cart, { 'cart created': (r) => r.status === 201 });

  const checkout = http.post(
    `${BASE_URL}/checkout`,
    JSON.stringify({ cartId: cart.json('id') }),
    params,
  );
  check(checkout, {
    'order confirmed': (r) => r.json('status') === 'confirmed',
  });
}
