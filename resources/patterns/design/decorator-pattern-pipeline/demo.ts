import { createHttpClient } from './src/httpClientFactory.js';

const client = createHttpClient({
  token: process.env.API_TOKEN ?? 'demo-token',
  maxRetries: 3,
});

const response = await client.request('https://jsonplaceholder.typicode.com/todos/1', {
  method: 'GET',
});

console.log('status:', response.status);
console.log('body:', await response.json());
