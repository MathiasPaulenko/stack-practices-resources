# Conectar a Redis

Companion ejecutable de la receta [Conectar a Redis](https://stackpractices.com/es/recipes/connect-to-redis/): conexión por URL, pools, pipelines, limitador de tasa, sorted sets y pub/sub en Python, JavaScript y Java.

## Contenido

- `docker-compose.yml` + `redis.conf` — Redis 7 local con `maxmemory` + `allkeys-lru` + AOF
- `connect.py` — `redis-py` `from_url` + `decode_responses` + pipeline + limitador `INCR`/`EXPIRE`
- `connect.js` — `ioredis` con URL + `retryStrategy` + sorted sets + pub/sub con una segunda conexión
- `RedisExample.java` — `JedisPooled` + `setex`/`hset` + limitador Lua
- `requirements.txt`, `package.json`

## Ejecutarlo

```bash
docker compose up -d          # levanta Redis en localhost:6379

# Python
pip install -r requirements.txt
python connect.py

# JavaScript
npm install
npm start

# Java — necesita jedis en el classpath
javac -cp ".:jedis.jar" RedisExample.java
java -cp ".:jedis.jar" RedisExample
```

## Notas

- La cadena de conexión viene de `REDIS_URL` (`redis://host:6379/0` en local). Nunca hardcodees credenciales de producción — usa `rediss://user:password@host:6379` para AUTH + TLS.
- En local no hay contraseña. En producción hacen falta usuarios ACL (`ACL SETUSER`) y TLS; los servicios gestionados te entregan un endpoint `rediss://`.
- `maxmemory` + una política de evicción son obligatorios en producción — sin ellos Redis crece hasta que el OOM killer lo elige. `allkeys-lru` para cachés, `noeviction` para datos durables.
- Usa `SCAN`/`HSCAN` en lugar de `KEYS`/`HGETALL` en keyspaces grandes — los comandos bloqueantes congelan el hilo único.
