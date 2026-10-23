# Companion de Sharding de Bases de Datos

Archivos companion de la guía [Guía Completa de Sharding de Bases de Datos](https://stackpractices.com/es/guides/complete-guide-database-sharding/).

Piezas ejecutables del ejemplo práctico: un router de shards por directorio y un script de migración de tenants para rebalancear un SaaS multi-tenant.

## Contenido

| Archivo | Qué muestra |
| ------- | ----------- |
| `shard-directory.sql` | Tabla `shard_directory` + datos semilla para ubicación regional |
| `shard-router.js` | `ShardRouter` que cachea el directorio y enruta consultas por `tenant_id` |
| `migrate-tenant.js` | `migrateTenant()`: copia filas, repunta el directorio, borra del shard viejo |

## Uso

Ambos módulos esperan pools compatibles con `pg` (`pool.query(sql, params)`).

```javascript
const { ShardRouter, shardMiddleware } = require("./shard-router");
const { migrateTenant } = require("./migrate-tenant");

const metaDb = /* Pool a la BD de metadatos */;
const pools = { 1: /* Pool shard1 */, 2: /* Pool shard2 */ };

const router = new ShardRouter(metaDb, pools);
await router.loadDirectory();

// Express: req.user.tenantId viene del JWT
app.use(shardMiddleware(router));

// Rebalanceo: mover el tenant 1002 del shard 1 al shard 4
await migrateTenant(1002, pools[1], pools[4], 4, metaDb);
await router.loadDirectory(); // recargar tras cambios en el directorio
```

## Notas

- `migrateTenant` no se coordina con escrituras en curso. En producción, pausa las escrituras del tenant o haz dual-write durante la ventana de copia.
- Invalidación de caché: cada ejecución de `migrateTenant` debe ir seguida de `loadDirectory()` (o un change feed) en cada instancia de la app.
