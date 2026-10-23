# Database Sharding Companion

Companion files for the guide [Complete Guide to Database Sharding](https://stackpractices.com/guides/complete-guide-database-sharding/).

Runnable pieces of the worked example: a directory-based shard router plus a tenant migration script for rebalancing a multi-tenant SaaS.

## Contents

| File | What it shows |
| ---- | ------------- |
| `shard-directory.sql` | `shard_directory` table + seed data for regional placement |
| `shard-router.js` | `ShardRouter` that caches the directory and routes queries by `tenant_id` |
| `migrate-tenant.js` | `migrateTenant()`: copy rows, repoint the directory, delete from the old shard |

## Usage

Both modules expect `pg`-compatible pool objects (`pool.query(sql, params)`).

```javascript
const { ShardRouter, shardMiddleware } = require("./shard-router");
const { migrateTenant } = require("./migrate-tenant");

const metaDb = /* Pool to the metadata DB */;
const pools = { 1: /* Pool shard1 */, 2: /* Pool shard2 */ };

const router = new ShardRouter(metaDb, pools);
await router.loadDirectory();

// Express: req.user.tenantId comes from the JWT
app.use(shardMiddleware(router));

// Rebalancing: move tenant 1002 from shard 1 to shard 4
await migrateTenant(1002, pools[1], pools[4], 4, metaDb);
await router.loadDirectory(); // reload after directory changes
```

## Notes

- `migrateTenant` does not coordinate with in-flight writes. In production, pause writes for the tenant or dual-write during the copy window.
- Cache invalidation: every `migrateTenant` run must be followed by `loadDirectory()` (or a change feed) on every app instance.
