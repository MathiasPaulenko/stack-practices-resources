# Patrón Two-Level Cache

Ejemplos ejecutables de [stackpractices.com/es/patterns/two-level-cache-pattern/](https://stackpractices.com/es/patterns/two-level-cache-pattern/).

| Archivo | Muestra |
|---------|---------|
| `two_level_cache.py` | L1 LRU con OrderedDict + L2 Redis + listener de invalidación pub/sub |
| `two-level-cache.ts` | L1 con Map + cliente `redis` para L2, publicación al invalidar |
| `TwoLevelCacheManager.java` | L1 Caffeine + L2 Jedis, publicación al invalidar |

## Ejecutar

```bash
python two_level_cache.py          # usa fakeredis si está instalado, si no Redis local
npx ts-node two-level-cache.ts     # necesita un Redis en ejecución
# Java: necesita caffeine + jedis + jackson-databind en el classpath
```

Idea clave: L1 es por instancia, así que las escrituras deben difundir las invalidaciones — `invalidate()` publica en `cache:invalidate` y cada instancia se suscribe en un hilo en segundo plano.
