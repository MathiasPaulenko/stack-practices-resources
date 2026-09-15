# refresh-ahead-cache-pattern

Recursos complementarios para la guía [Patrón Refresh-Ahead Cache](https://stackpractices.com/es/patterns/refresh-ahead-cache-pattern/) en StackPractices.com.

## Archivos

| Archivo | Lenguaje | Propósito |
|---------|----------|-----------|
| `refresh_ahead_cache.py` | Python | Clase RefreshAheadCache con hilo en segundo plano |
| `refresh_ahead_cache.ts` | TypeScript | Clase RefreshAheadCache con setInterval |
| `RefreshAheadCacheManager.java` | Java | RefreshAheadCacheManager con ScheduledExecutorService |

## Requisitos

### Python
- Python 3.9+
- redis >= 4.0 (`pip install redis`)

### TypeScript
- TypeScript 5+
- redis >= 4.0 (`npm install redis`)

### Java
- Java 17+
- jedis >= 5.0
- jackson-databind >= 2.15

## Uso

### Python
```bash
pip install redis
python refresh_ahead_cache.py
```

### TypeScript
```bash
npm install redis
npx ts-node refresh_ahead_cache.ts
```

### Java
```bash
javac -cp jedis.jar:jackson.jar RefreshAheadCacheManager.java
java -cp .:jedis.jar:jackson.jar RefreshAheadCacheManager
```
