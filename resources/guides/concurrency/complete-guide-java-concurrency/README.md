# Complete Guide to Java Concurrency — Companion Resources

Runnable Java examples for the guide
[Complete Guide to Java Concurrency](https://stackpractices.com/guides/complete-guide-java-concurrency/).

## Contents

| File | Purpose |
| --- | --- |
| `src/ExecutorExamples.java` | Bounded `ThreadPoolExecutor` + `CallerRunsPolicy` backpressure, graceful shutdown, virtual-thread-per-task executor |
| `src/CircuitBreaker.java` | Circuit breaker built on `CompletableFuture` |
| `tests/ConcurrencyTest.java` | JUnit contention tests — invariants, not scheduling |

## Usage

```bash
javac -d out src/*.java && java -cp out ExecutorExamples
# tests: JUnit 5 on classpath
```
