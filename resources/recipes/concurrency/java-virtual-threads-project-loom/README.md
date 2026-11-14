# Java Virtual Threads — Companion Code

Runnable versions of the examples from the StackPractices recipe
[Scale Concurrent Applications with Java Virtual Threads](https://stackpractices.com/recipes/java-virtual-threads-project-loom/).

Requires **JDK 21+** for virtual threads. The `StructuredTaskScope` examples
target the **JDK 25** preview API (JEP 505) and need `--enable-preview`;
`ScopedValue` is final in JDK 25 but preview on 21–24. Everything else runs
with no flags.

## Files

| File | Shows |
| --- | --- |
| `BasicVirtualThread.java` | `Thread.ofVirtual()`, naming, `join()`, `isVirtual()` |
| `VirtualThreadExecutor.java` | `Executors.newVirtualThreadPerTaskExecutor()`, 10,000 tasks, try-with-resources shutdown |
| `VirtualThreadIO.java` | Blocking `HttpClient` calls fanned out on virtual threads |
| `StructuredConcurrency.java` | `StructuredTaskScope.open()` default policy, `Subtask`, `FailedException` |
| `FirstResultPattern.java` | `Joiner.anySuccessfulResultOrThrow()` — first success wins, rest cancelled |
| `ScopedValueExample.java` | `ScopedValue` bindings inherited by forked virtual threads |
| `MixedThreads.java` | CPU-bound on a fixed pool + I/O-bound on virtual threads |
| `LockingExample.java` | `ReentrantLock` for lock features; pinning is fixed since JDK 24 (JEP 491) |
| `BoundedVirtualThreads.java` | `Semaphore` to cap fan-out against a limited downstream |

## Compile and run

```bash
# Plain virtual threads — JDK 21+, no flags
javac BasicVirtualThread.java VirtualThreadExecutor.java VirtualThreadIO.java \
      MixedThreads.java LockingExample.java BoundedVirtualThreads.java
java VirtualThreadExecutor

# Structured concurrency + scoped values — JDK 25 preview
javac --release 25 --enable-preview StructuredConcurrency.java FirstResultPattern.java
java --enable-preview StructuredConcurrency
java --enable-preview FirstResultPattern

# ScopedValue — no flags on JDK 25, --enable-preview on JDK 21–24
javac ScopedValueExample.java && java ScopedValueExample
```

`VirtualThreadIO` hits `httpbin.org` — it needs network access. To inspect
virtual threads in a running app:

```bash
jcmd <pid> Thread.dump_to_file -format=json threads.json
# virtual threads appear with "virtual": true, grouped by owning scope
```

## Notes

- `StructuredTaskScope.open()` covers the common "wait all, propagate first
  failure" policy. For a stream of results use
  `Joiner.allSuccessfulOrThrow()`; for first-success-wins use
  `Joiner.anySuccessfulResultOrThrow()`.
- On JDK 21–24 the same scopes use the constructor API
  (`new StructuredTaskScope.ShutdownOnFailure()` /
  `ShutdownOnSuccess<>()`), removed in JDK 25.
- Pinning: `synchronized` pinned virtual threads on JDK 21–23; JEP 491
  removed that in JDK 24. Native and foreign (FFM) calls still pin.
