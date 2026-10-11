// Path traversal guard — run: node path_traversal_guard.js
// Resolves a user-supplied path under an allowed base and rejects escapes.

const path = require('path');

const ALLOWED_BASE = path.resolve(__dirname, 'uploads');

function resolveUserPath(userPath) {
  const normalized = path.normalize(path.resolve(ALLOWED_BASE, userPath));

  if (!normalized.startsWith(ALLOWED_BASE + path.sep)) {
    throw new Error('Path traversal detected');
  }
  if (userPath.includes('\0')) {
    throw new Error('Null byte in path');
  }
  return normalized;
}

// Demo
for (const attempt of ['reports/2024/q1.pdf', '../../etc/passwd', 'a\0b.pdf']) {
  try {
    console.log(`OK   ${JSON.stringify(attempt)} -> ${resolveUserPath(attempt)}`);
  } catch (err) {
    console.log(`BLOCK ${JSON.stringify(attempt)} -> ${err.message}`);
  }
}
