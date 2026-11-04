# Guía Completa de Concurrencia en Java — Recursos complementarios

Ejemplos Java ejecutables para la guía
[Guía Completa de Concurrencia en Java](https://stackpractices.com/es/guides/complete-guide-java-concurrency/).

## Contenido

| Archivo | Propósito |
| --- | --- |
| `src/ExecutorExamples.java` | `ThreadPoolExecutor` acotado + backpressure con `CallerRunsPolicy`, apagado limpio, executor de virtual thread por tarea |
| `src/CircuitBreaker.java` | Circuit breaker construido sobre `CompletableFuture` |
| `tests/ConcurrencyTest.java` | Tests JUnit de contención — invariantes, no scheduling |

## Uso

```bash
javac -d out src/*.java && java -cp out ExecutorExamples
# tests: JUnit 5 en el classpath
```
