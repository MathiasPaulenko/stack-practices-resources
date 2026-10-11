// NoSQL query operator stripping — run: node nosql_sanitize.js
// Removes $-prefixed operators from user-supplied query objects.

function sanitizeQuery(obj) {
  const cleaned = {};
  for (const [key, value] of Object.entries(obj)) {
    if (key.startsWith('$')) {
      continue; // Strip $where, $gt, $ne, etc.
    }
    cleaned[key] =
      typeof value === 'object' && value !== null ? sanitizeQuery(value) : value;
  }
  return cleaned;
}

// Demo
const hostile = { username: { $ne: null }, password: { $gt: '' }, name: 'alice' };
console.log('input :', JSON.stringify(hostile));
console.log('output:', JSON.stringify(sanitizeQuery(hostile)));
// output: {"username":{},"password":{},"name":"alice"}
