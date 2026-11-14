# Composición con Java CompletableFuture — Código Companion

Versiones ejecutables de los pipelines de la receta de StackPractices
[Componer Pipelines Asíncronos con Java CompletableFuture](https://stackpractices.com/es/recipes/java-completable-future-composition/).

Requiere **Java 17+** (`orTimeout`, `completeOnTimeout`, `delayedExecutor`, `failedFuture`, records, `HttpClient`).

## Archivos

| Archivo | Muestra |
| --- | --- |
| `AsyncApiClient.java` | `HttpClient.sendAsync` → `CompletableFuture`, `thenApply`, `join()` |
| `UserService.java` | Capa de obtención/parseo compartida sobre la que se componen los pipelines |
| `SequentialPipeline.java` | `thenCompose` — las llamadas dependientes quedan planas |
| `ParallelCombination.java` | `thenCombine` — unir futures independientes de a pares |
| `AllOfPattern.java` | fan-out con `allOf`, agregación tipada, semántica de fallo rápido, fuentes opcionales vía `exceptionally` |
| `AnyOfPattern.java` | competencia con `anyOf`, primera completación vs primer éxito con filtro `exceptionally` |
| `ErrorHandling.java` | `exceptionally` / `handle` / `whenComplete`, `failedFuture` para propagar el último error |
| `CustomExecutorExample.java` | Pool dedicado vs `ForkJoinPool.commonPool()`, fijar etapas con `*Async`, shutdown del executor |
| `TimeoutExample.java` | `orTimeout` vs `completeOnTimeout` — ninguno cancela la llamada subyacente |
| `RetryWithBackoff.java` | Reintento asíncrono en `delayedExecutor`, `failedFuture` en el último intento |
| `Models.java` | Records de dominio compartidos por todos los ejemplos |

## Compilar

```bash
javac *.java
```

Los métodos `main` apuntan a `api.example.com`, que no resuelve — compilan
y muestran la forma de llamada prevista. Apuntalos a un endpoint real (o a
un mock local) para verlos correr.

## Notas

- `anyOf` resuelve con la primera *completación*, no con el primer éxito —
  ver `fetchFirstAvailable` para el filtro `exceptionally(ex -> null)`.
- `allOf` falla rápido pero no cancela a los rezagados; engancha handlers
  por future cuando los resultados parciales son aceptables.
- `orTimeout`/`completeOnTimeout` actúan solo sobre el future; cancelar la
  petición HTTP requiere `cancel(true)` sobre el future de `sendAsync`.
