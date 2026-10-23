// migrate-tenant.js
// Move one tenant from one shard to another (rebalancing step).
// Companion to: https://stackpractices.com/guides/complete-guide-database-sharding/
//
// Order matters: copy rows, update the directory, then delete the source
// rows. Run this while writes for that tenant are paused or dual-written —
// this naive version does not handle in-flight writes.

async function migrateTenant(tenantId, from, to, newShardId, metaDb) {
  const tables = ["users", "orders", "invoices"];

  // 1. Copy the tenant's rows to the new shard.
  for (const t of tables) {
    const { rows } = await from.query(
      `SELECT * FROM ${t} WHERE tenant_id = $1`, [tenantId]);
    for (const row of rows) {
      const cols = Object.keys(row);
      const ph = cols.map((_, i) => `$${i + 1}`).join(",");
      await to.query(
        `INSERT INTO ${t} (${cols.join(",")}) VALUES (${ph})`,
        Object.values(row));
    }
  }

  // 2. Point the tenant at the new shard before deleting old data,
  //    so a router reload never routes to a shard that no longer
  //    has the tenant's rows.
  await metaDb.query(
    "UPDATE shard_directory SET shard_id = $1 WHERE tenant_id = $2",
    [newShardId, tenantId]);

  // 3. Delete the tenant's rows from the old shard.
  for (const t of tables) {
    await from.query(`DELETE FROM ${t} WHERE tenant_id = $1`, [tenantId]);
  }
}

module.exports = { migrateTenant };
