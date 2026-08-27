# Thread-Safe Collections Examples

Runnable companion code for the StackPractices recipe [Thread-Safe Collections: Blocking Queues and Concurrent Maps](https://stackpractices.com/recipes/concurrent-data-structures/).

## Files

- `OrderProcessor.java` — producer-consumer with `ArrayBlockingQueue`.
- `InMemoryCache.java` — lazy loading with `ConcurrentHashMap`.
- `CopyOnWriteEventDispatcher.java` — listener list with `CopyOnWriteArrayList`.
- `TaskQueue.py` — producer-consumer with Python `queue.Queue`.
- `AtomicCounter.py` — counter protected with `threading.Lock`.
- `AtomicCounter.cpp` — counter with C++ `std::atomic`.

## Running

### Java

```bash
javac OrderProcessor.java && java OrderProcessor
javac InMemoryCache.java && java InMemoryCache
javac CopyOnWriteEventDispatcher.java && java CopyOnWriteEventDispatcher
```

### Python

```bash
python TaskQueue.py
python AtomicCounter.py
```

### C++

```bash
g++ -std=c++17 AtomicCounter.cpp -o atomic-counter -pthread
./atomic-counter
```
