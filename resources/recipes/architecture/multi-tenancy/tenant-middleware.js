// Resolve the tenant once per request and attach it to req.
// Express exposes req.subdomains (an array), not req.subdomain.
function tenantMiddleware(req, res, next) {
  const tenantId = req.headers['x-tenant-id'] || req.subdomains[0];

  if (!tenantId) {
    return res.status(400).json({ error: 'Tenant ID required' });
  }

  req.tenantId = tenantId;
  next();
}

// Scope the DB session to the tenant inside a transaction. SET LOCAL
// lasts only for that transaction, so a pooled connection can't leak
// tenant context to the next request that reuses it.
async function withTenant(pool, tenantId, fn) {
  const client = await pool.connect();
  try {
    await client.query('BEGIN');
    await client.query('SELECT set_config($1, $2, true)', ['app.current_tenant', tenantId]);
    const result = await fn(client);
    await client.query('COMMIT');
    return result;
  } catch (err) {
    await client.query('ROLLBACK');
    throw err;
  } finally {
    client.release();
  }
}

module.exports = { tenantMiddleware, withTenant };
