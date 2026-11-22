import { Pool, PoolClient } from 'pg';

interface TenantDatabase {
  pool: Pool;
  schema: string;
}

class TenantConnectionManager {
  private pools: Map<string, TenantDatabase> = new Map();

  async getTenantConnection(tenantId: string): Promise<PoolClient> {
    let tenantDb = this.pools.get(tenantId);

    if (!tenantDb) {
      const pool = new Pool({
        host: process.env.DB_HOST,
        port: 5432,
        database: `tenant_${tenantId}`,
        user: process.env.DB_USER,
        password: process.env.DB_PASSWORD,
        max: 10,
        idleTimeoutMillis: 30000,
      });
      tenantDb = { pool, schema: 'public' };
      this.pools.set(tenantId, tenantDb);
    }

    const client = await tenantDb.pool.connect();
    await client.query('SET search_path TO public');
    return client;
  }

  async closeTenant(tenantId: string): Promise<void> {
    const tenantDb = this.pools.get(tenantId);
    if (tenantDb) {
      await tenantDb.pool.end();
      this.pools.delete(tenantId);
    }
  }

  async closeAll(): Promise<void> {
    const promises = Array.from(this.pools.values()).map((db) => db.pool.end());
    await Promise.all(promises);
    this.pools.clear();
  }
}

// One manager per process — pooling only works if the Map
// survives across requests.
const tenantManager = new TenantConnectionManager();

export async function getOrder(tenantId: string, orderId: string) {
  const client = await tenantManager.getTenantConnection(tenantId);
  try {
    const result = await client.query('SELECT * FROM orders WHERE id = $1', [orderId]);
    return result.rows[0];
  } finally {
    client.release();
  }
}
