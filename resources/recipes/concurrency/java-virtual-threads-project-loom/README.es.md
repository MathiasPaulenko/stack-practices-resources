# Hilos Virtuales de Java — Código Complementario

Versiones ejecutables de los ejemplos de la receta de StackPractices
[Escalar Aplicaciones Concurrentes con Java Virtual Threads](https://stackpractices.com/es/recipes/java-virtual-threads-project-loom/).

Requiere **JDK 21+** para hilos virtuales. Los ejemplos de `StructuredTaskScope`
usan la API preview de **JDK 25** (JEP 505) y necesitan `--enable-preview`;
`ScopedValue` es final en JDK 25 pero preview en 21–24. Todo lo demás corre
sin flags.

## Archivos

| Archivo | Muestra |
| --- | --- |
| `BasicVirtualThread.java` | `Thread.ofVirtual()`, naming, `join()`, `isVirtual()` |
| `VirtualThreadExecutor.java` | `Executors.newVirtualThreadPerTaskExecutor()`, 10,000 tareas, cierre con try-with-resources |
| `VirtualThreadIO.java` | Llamadas `HttpClient` bloqueantes repartidas en hilos virtuales |
| `StructuredConcurrency.java` | `StructuredTaskScope.open()` política por defecto, `Subtask`, `FailedException` |
| `FirstResultPattern.java` | `Joiner.anySuccessfulResultOrThrow()` — gana el primer éxito, el resto se cancela |
| `ScopedValueExample.java` | Bindings de `ScopedValue` heredados por hilos virtuales hijos |
| `MixedThreads.java` | CPU-bound en pool fijo + I/O-bound en hilos virtuales |
| `LockingExample.java` | `ReentrantLock` por sus funciones; el pinning se arregló en JDK 24 (JEP 491) |
| `BoundedVirtualThreads.java` | `Semaphore` para acotar el fan-out contra un downstream limitado |

## Compilar y ejecutar

```bash
# Hilos virtuales planos — JDK 21+, sin flags
javac BasicVirtualThread.java VirtualThreadExecutor.java VirtualThreadIO.java \
      MixedThreads.java LockingExample.java BoundedVirtualThreads.java
java VirtualThreadExecutor

# Concurrencia estructurada + scoped values — preview de JDK 25
javac --release 25 --enable-preview StructuredConcurrency.java FirstResultPattern.java
java --enable-preview StructuredConcurrency
java --enable-preview FirstResultPattern

# ScopedValue — sin flags en JDK 25, --enable-preview en JDK 21–24
javac ScopedValueExample.java && java ScopedValueExample
```

`VirtualThreadIO` llama a `httpbin.org` — necesita red. Para inspeccionar
hilos virtuales en una app corriendo:

```bash
jcmd <pid> Thread.dump_to_file -format=json threads.json
# los hilos virtuales aparecen con "virtual": true, agrupados por su scope
```

## Notas

- `StructuredTaskScope.open()` cubre la política común "esperar todo, propagar
  el primer fallo". Para un stream de resultados usa
  `Joiner.allSuccessfulOrThrow()`; para gana-el-primero usa
  `Joiner.anySuccessfulResultOrThrow()`.
- En JDK 21–24 los mismos scopes usan la API de constructores
  (`new StructuredTaskScope.ShutdownOnFailure()` /
  `ShutdownOnSuccess<>()`), eliminada en JDK 25.
- Pinning: `synchronized` pineaba hilos virtuales en JDK 21–23; JEP 491 lo
  eliminó en JDK 24. Las llamadas nativas y foráneas (FFM) sí siguen pineando.
