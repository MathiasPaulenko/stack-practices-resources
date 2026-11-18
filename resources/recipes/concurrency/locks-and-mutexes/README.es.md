# Ejemplos de Locks, Mutexes y Semáforos

Código ejecutable de acompañamiento para la receta de StackPractices [Coordinar acceso compartido con locks, mutexes y semáforos](https://stackpractices.com/recipes/locks-and-mutexes/).

## Archivos

- `BankAccount.java` — exclusión mutua con `ReentrantLock`; 4 threads x 25.000 depósitos deben totalizar $100.000.
- `CachedData.java` — read-write lock con `ReentrantReadWriteLock`; los lectores corren en paralelo y un escritor refresca el cache.
- `ConnectionPool.py` — pool de recursos acotado con `threading.Semaphore`; 5 workers comparten 3 conexiones.
- `AtomicCounter.cpp` — contador lock-free con `std::atomic`; 4 threads x 100.000 incrementos deben totalizar 400.000.

## Ejecución

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
