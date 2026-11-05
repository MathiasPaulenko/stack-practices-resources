// Companion: warm-connection reuse pattern for TCP databases in Lambda
// Client initialized OUTSIDE the handler — persists across warm invocations.
import pg from 'pg';
const pool = new pg.Pool({ max: 1, connectionString: process.env.DATABASE_URL });

export const handler = async (event) => {
  const { rows } = await pool.query('SELECT 1');
  return { statusCode: 200, body: JSON.stringify(rows) };
};
// Rule: never `new Client()` + connect() INSIDE the handler — that is a fresh
// TCP+TLS+auth handshake per invocation and the reason RDS Proxy exists.
