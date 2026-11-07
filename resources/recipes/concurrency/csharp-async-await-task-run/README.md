# C# async/await & Task.Run — Companion Code

Runnable examples for the [C# async/await recipe](https://stackpractices.com/recipes/csharp-async-await-task-run/) on StackPractices.

| File | What it shows |
|------|---------------|
| `AsyncFanOut.cs` | `Task.WhenAll` fan-out and `WhenAny` timeout with proper loser cancellation |
| `ChannelPipeline.cs` | Bounded `Channel<T>` producer-consumer with backpressure |
| `BoundedParallelism.cs` | `Parallel.ForEachAsync` and `SemaphoreSlim` rate limiting |
| `CancellationDemo.cs` | Cooperative cancellation with `CancellationTokenSource` |
| `AsyncStreams.cs` | `IAsyncEnumerable` streaming with cancellation |

## Run

Each file has its own `Main` and targets .NET 8+. Run one at a time:

```bash
dotnet run AsyncFanOut.cs        # uses httpbin.org — needs network
dotnet run ChannelPipeline.cs    # self-contained
dotnet run BoundedParallelism.cs # needs network
dotnet run CancellationDemo.cs   # self-contained
dotnet run AsyncStreams.cs       # self-contained
```

Or drop them into a console project (`dotnet new console`) and keep the `Main` you want.
