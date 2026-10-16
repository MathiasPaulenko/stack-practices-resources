// Reuse a small pool across warm Lambda invocations.
// Module-level init runs once per execution environment; the proxy
// (RDS Proxy / PgBouncer) does the real multiplexing.
// See https://stackpractices.com/guides/connection-pooling-deep-dive-guide/
const { Pool } = require('pg');

let pool;
function getPool() {
  if (!pool) {
    pool = new Pool({
      connectionString: process.env.DATABASE_URL, // points at the proxy
      max: 2,                    // tiny on purpose
      idleTimeoutMillis: 10000,
      allowExitOnIdle: true,
    });
  }
  return pool;
}

exports.handler = async (event) => {
  const client = await getPool().connect();
  try {
    const result = await client.query('SELECT 1');
    return { statusCode: 200, body: JSON.stringify(result.rows) };
  } finally {
    client.release(); // return to the pool, do not end()
  }
};
