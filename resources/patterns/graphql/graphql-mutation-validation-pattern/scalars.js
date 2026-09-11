// scalars.js — Custom GraphQL scalar helpers (JS version, dependency-free).

function isValidEmail(value) {
  return typeof value === "string" && /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
}

function normalizeEmail(value) {
  return value.toLowerCase().trim();
}

module.exports = { isValidEmail, normalizeEmail };
