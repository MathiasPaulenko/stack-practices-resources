// Lambda + RDS Proxy: max=1 per instance — the proxy multiplexes globally.
import pkg from "pg";
const { Pool } = pkg;

let pool = null;

function getPool() {
  if (!pool) {
    pool = new Pool({
      host: process.env.DB_HOST,        // RDS Proxy endpoint
      port: 5432,
      database: process.env.DB_NAME,
      user: process.env.DB_USER,
      password: process.env.DB_PASSWORD,
      max: 1,
      idleTimeoutMillis: 30000,
      connectionTimeoutMillis: 3000,
      ssl: { rejectUnauthorized: true },
    });
    console.log("[POOL] Created pool (max=1)");
  }
  return pool;
}

export const handler = async (event) => {
  const client = await getPool().connect();
  try {
    const res = await client.query(
      "SELECT id, email FROM users WHERE id = $1",
      [event.pathParameters.id]
    );
    return { statusCode: 200, body: JSON.stringify(res.rows[0]) };
  } finally {
    client.release();
  }
};
