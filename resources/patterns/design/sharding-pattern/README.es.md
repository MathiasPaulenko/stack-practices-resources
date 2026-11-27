# Patrón de Sharding

Código companion de [Patrón de Sharding: Divide los Datos entre Servidores](https://stackpractices.com/es/patterns/sharding-pattern/) en StackPractices.

Tres estrategias de enrutado, una por lenguaje:

| Archivo | Estrategia | Notas |
|---------|------------|-------|
| `shard_manager.py` | Por hash (`hash(key) % N`) | `ShardManager` de Redis con operaciones por clave y `mget` agrupado |
| `directory_shard_manager.js` | Por directorio | Enrutado por tabla de búsqueda con `migrateEntity` en vivo entre shards |
| `RangeShardRouter.java` | Por rango | Router Spring `JdbcTemplate` sobre límites de IDs contiguos |

## Requisitos

- `shard_manager.py` — Python 3.8+, paquete `redis`, instancias de Redis accesibles en `redis-1..3:6379`.
- `directory_shard_manager.js` — Node.js 18+; espera objetos de pool de conexiones (`usEastPool`, `euWestPool`, `apSouthPool`) que expongan `query(sql, params)`.
- `RangeShardRouter.java` — contexto de Spring que aporte la lista de `DataSource` y la lista de límites.

Ninguno de estos archivos incluye las conexiones — son la capa de enrutado que colocarías delante de pools reales.
