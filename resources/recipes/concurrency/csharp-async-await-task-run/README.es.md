# C# async/await y Task.Run — Código Companion

Ejemplos ejecutables de la [receta C# async/await](https://stackpractices.com/es/recipes/csharp-async-await-task-run/) en StackPractices.

| Archivo | Qué muestra |
|---------|-------------|
| `AsyncFanOut.cs` | Fan-out con `Task.WhenAll` y timeout con `WhenAny` cancelando la perdedora |
| `ChannelPipeline.cs` | Productor-consumidor con `Channel<T>` acotado y backpressure |
| `BoundedParallelism.cs` | Rate limiting con `Parallel.ForEachAsync` y `SemaphoreSlim` |
| `CancellationDemo.cs` | Cancelación cooperativa con `CancellationTokenSource` |
| `AsyncStreams.cs` | Streaming con `IAsyncEnumerable` y cancelación |

## Ejecutar

Cada archivo tiene su propio `Main` y apunta a .NET 8+. Ejecuta uno cada vez:

```bash
dotnet run AsyncFanOut.cs        # usa httpbin.org — necesita red
dotnet run ChannelPipeline.cs    # autocontenido
dotnet run BoundedParallelism.cs # necesita red
dotnet run CancellationDemo.cs   # autocontenido
dotnet run AsyncStreams.cs       # autocontenido
```

O mételos en un proyecto de consola (`dotnet new console`) y conserva el `Main` que quieras.
