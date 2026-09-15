# refresh-ahead-cache-pattern

Companion resources for the [Refresh-Ahead Cache Pattern](https://stackpractices.com/patterns/refresh-ahead-cache-pattern/) guide on StackPractices.com.

## Files

| File | Language | Purpose |
|------|----------|---------|
| `refresh_ahead_cache.py` | Python | RefreshAheadCache class with background thread |
| `refresh_ahead_cache.ts` | TypeScript | RefreshAheadCache class with setInterval |
| `RefreshAheadCacheManager.java` | Java | RefreshAheadCacheManager with ScheduledExecutorService |

## Requirements

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

## Usage

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
