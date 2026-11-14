# Java CompletableFuture Composition — Companion Code

Runnable versions of the pipelines from the StackPractices recipe
[Compose Asynchronous Pipelines with Java CompletableFuture](https://stackpractices.com/recipes/java-completable-future-composition/).

Requires **Java 17+** (`orTimeout`, `completeOnTimeout`, `delayedExecutor`, `failedFuture`, records, `HttpClient`).

## Files

| File | Shows |
| --- | --- |
| `AsyncApiClient.java` | `HttpClient.sendAsync` → `CompletableFuture`, `thenApply`, `join()` |
| `UserService.java` | Shared fetch/parse layer the pipelines compose over |
| `SequentialPipeline.java` | `thenCompose` — dependent calls stay flat |
| `ParallelCombination.java` | `thenCombine` — merging independent futures pairwise |
| `AllOfPattern.java` | `allOf` fan-out, typed aggregation, fail-fast semantics, optional sources via `exceptionally` |
| `AnyOfPattern.java` | `anyOf` racing, first-completion vs first-success with an `exceptionally` filter |
| `ErrorHandling.java` | `exceptionally` / `handle` / `whenComplete`, `failedFuture` for propagating the last error |
| `CustomExecutorExample.java` | Dedicated pool vs `ForkJoinPool.commonPool()`, `*Async` stage pinning, executor shutdown |
| `TimeoutExample.java` | `orTimeout` vs `completeOnTimeout` — neither cancels the underlying call |
| `RetryWithBackoff.java` | Async retry on `delayedExecutor`, `failedFuture` on the last attempt |
| `Models.java` | Domain records shared by all examples |

## Compile

```bash
javac *.java
```

The `main` methods hit `api.example.com`, which doesn't resolve — they compile
and show the intended call shape. Point them at a real endpoint (or a local
mock) to see them run.

## Notes

- `anyOf` resolves on the first *completion*, not the first success — see
  `fetchFirstAvailable` for the `exceptionally(ex -> null)` filter.
- `allOf` fails fast but doesn't cancel stragglers; attach per-future
  handlers when partial results are acceptable.
- `orTimeout`/`completeOnTimeout` act on the future only; cancelling the
  HTTP request needs `cancel(true)` on the `sendAsync` future.
