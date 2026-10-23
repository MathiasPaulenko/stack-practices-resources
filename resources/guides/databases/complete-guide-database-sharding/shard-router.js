// shard-router.js
// Directory-based shard router for a multi-tenant SaaS.
// Companion to: https://stackpractices.com/guides/complete-guide-database-sharding/
//
// The router loads shard_directory once and caches tenant -> pool in memory,
// so lookups do not add a round-trip per query. Call loadDirectory() again
// (or subscribe to a change feed) after rebalancing.

class ShardRouter {
  constructor(metaDb, pools) {
    this.metaDb = metaDb; // connection to the metadata DB holding shard_directory
    this.pools = pools;   // { shardId: pg.Pool }
    this.shards = new Map();
  }

  async loadDirectory() {
    const { rows } = await this.metaDb.query(
      "SELECT tenant_id, shard_id FROM shard_directory"
    );
    for (const r of rows) {
      this.shards.set(r.tenant_id, this.pools[r.shard_id]);
    }
  }

  getShard(tenantId) {
    const pool = this.shards.get(tenantId);
    if (!pool) throw new Error(`Tenant not found: ${tenantId}`);
    return pool;
  }

  async query(tenantId, sql, params) {
    return this.getShard(tenantId).query(sql, params);
  }
}

// Express middleware: extracts tenant_id from the JWT and attaches the
// tenant's shard pool to the request.
function shardMiddleware(shardRouter) {
  return (req, res, next) => {
    try {
      req.db = shardRouter.getShard(req.user.tenantId);
      next();
    } catch (err) {
      next(err);
    }
  };
}

module.exports = { ShardRouter, shardMiddleware };
