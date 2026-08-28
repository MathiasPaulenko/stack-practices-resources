// URL encoding and decoding examples in JavaScript

function encodeValue(value) {
  return encodeURIComponent(value);
}

function buildQueryString(params) {
  return new URLSearchParams(params).toString();
}

function parseUrl(url) {
  const parsed = new URL(url);
  const result = {};
  for (const [key, value] of parsed.searchParams.entries()) {
    result[key] = value;
  }
  return result;
}

function decodeValue(encoded) {
  return decodeURIComponent(encoded);
}

// Encode
const encoded = encodeValue("hello world & friends");
console.log(`Encoded: ${encoded}`); // hello%20world%20%26%20friends

// Build query string
const query = buildQueryString({ search: "python & java", page: "2" });
console.log(`Query: ${query}`); // search=python+%26+java&page=2

// Parse URL
const params = parseUrl("https://api.example.com/search?query=hello%20world&limit=10");
console.log(`Parsed:`, params); // { query: 'hello world', limit: '10' }

// Decode
const decoded = decodeValue("hello%20world");
console.log(`Decoded: ${decoded}`); // hello world
