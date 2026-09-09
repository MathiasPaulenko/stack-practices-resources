# Distributed Lock Pattern

Companion code for the StackPractices [Distributed Lock Pattern](https://stackpractices.com/patterns/distributed-lock-pattern/).

## Files

| File | Language | Description |
|------|----------|-------------|
| `redis_lock.py` | Python | Redis SET NX lock with TTL and fencing token |
| `redlock.js` | JavaScript | Redis SET NX lock using ioredis |
| `ZooKeeperLock.java` | Java | ZooKeeper lock via Apache Curator InterProcessMutex |
| `test_redis_lock.py` | Python | Unit tests for the Python lock using a fake Redis |

## Running the Tests

```bash
cd resources/patterns/design/distributed-lock-pattern
pip install pytest
pytest -v
```

## Key Concepts

- **TTL**: Every lock has a time-to-live so a crashed holder cannot deadlock the system.
- **Fencing token**: A UUID tied to each acquisition, sent with every write so delayed writes can be rejected.
- **Atomic release**: A Lua script checks the token before deleting the key, preventing accidental release of someone else's lock.
- **Redlock**: Acquires the same lock on multiple Redis nodes and treats it as held only with a quorum.

## Related

- [Distributed Lock Pattern (EN)](https://stackpractices.com/patterns/distributed-lock-pattern/)
- [Patrón Distributed Lock (ES)](https://stackpractices.com/es/patterns/distributed-lock-pattern/)
- [Redis distributed locks docs](https://redis.io/docs/manual/patterns/distributed-locks/)
- [Apache Curator](https://curator.apache.org/)
- [Martin Kleppmann on Redlock](https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html)
