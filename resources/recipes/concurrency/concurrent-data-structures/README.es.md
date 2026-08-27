# Ejemplos de Colecciones Thread-Safe

Código ejecutable de acompañamiento para la receta de StackPractices [Colecciones Thread-Safe: Blocking Queues y Concurrent Maps](https://stackpractices.com/recipes/concurrent-data-structures/).

## Archivos

- `OrderProcessor.java` — productor-consumidor con `ArrayBlockingQueue`.
- `InMemoryCache.java` — carga perezosa con `ConcurrentHashMap`.
- `CopyOnWriteEventDispatcher.java` — lista de listeners con `CopyOnWriteArrayList`.
- `TaskQueue.py` — productor-consumidor con `queue.Queue` de Python.
- `AtomicCounter.py` — contador protegido con `threading.Lock`.
- `AtomicCounter.cpp` — contador con `std::atomic` en C++.

## Ejecución

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
