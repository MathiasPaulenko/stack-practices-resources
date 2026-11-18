# Locks, Mutexes, and Semaphores Examples

Runnable companion code for the StackPractices recipe [Coordinate Shared Access with Locks, Mutexes, and Semaphores](https://stackpractices.com/recipes/locks-and-mutexes/).

## Files

- `BankAccount.java` — mutual exclusion with `ReentrantLock`; 4 threads x 25,000 deposits must total $100,000.
- `CachedData.java` — read-write lock with `ReentrantReadWriteLock`; readers run in parallel, one writer refreshes the cache.
- `ConnectionPool.py` — bounded resource pool with `threading.Semaphore`; 5 workers share 3 connections.
- `AtomicCounter.cpp` — lock-free counter with `std::atomic`; 4 threads x 100,000 increments must total 400,000.

## Running

### Java

```bash
javac BankAccount.java && java BankAccount
javac CachedData.java && java CachedData
```

### Python

```bash
python ConnectionPool.py
```

### C++

```bash
g++ -std=c++17 AtomicCounter.cpp -o atomic-counter -pthread
./atomic-counter
```
