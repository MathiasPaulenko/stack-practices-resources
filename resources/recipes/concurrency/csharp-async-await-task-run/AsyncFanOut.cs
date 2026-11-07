// Fan-out / fan-in with Task.WhenAll, and a timeout race with Task.WhenAny.
// Build: dotnet run AsyncFanOut.cs  (or csc AsyncFanOut.cs && AsyncFanOut)
// Requires: .NET 8+

using System.Diagnostics;

public static class AsyncFanOut
{
    // Reuse HttpClient — one per call exhausts sockets under load.
    private static readonly HttpClient client = new();

    public static async Task<string> FetchDataAsync(string url, CancellationToken ct = default)
        => await client.GetStringAsync(url, ct);

    public static async Task RunWhenAllAsync()
    {
        var sw = Stopwatch.StartNew();
        var urls = Enumerable.Range(1, 5)
            .Select(i => "https://httpbin.org/delay/1")
            .ToArray();

        var results = await Task.WhenAll(urls.Select(FetchDataAsync));

        Console.WriteLine($"Parallel: {sw.ElapsedMilliseconds}ms, {results.Length} responses");
    }

    /// <summary>
    /// Race a fetch against a timeout. The loser is cancelled so it does not
    /// run on unobserved — abandoned faulted tasks can surface as
    /// TaskScheduler.UnobservedTaskException later.
    /// </summary>
    public static async Task<string> FetchWithTimeoutAsync(string url, TimeSpan timeout)
    {
        using var cts = new CancellationTokenSource();
        var fetchTask = FetchDataAsync(url, cts.Token);
        var timeoutTask = Task.Delay(timeout, cts.Token);

        var completed = await Task.WhenAny(fetchTask, timeoutTask);

        if (completed == timeoutTask)
        {
            cts.Cancel();
            throw new TimeoutException($"Request to {url} timed out after {timeout}");
        }

        cts.Cancel();
        return await fetchTask;
    }

    public static async Task Main()
    {
        await RunWhenAllAsync();

        try
        {
            var result = await FetchWithTimeoutAsync(
                "https://httpbin.org/delay/5", TimeSpan.FromSeconds(2));
            Console.WriteLine(result.Length + " bytes");
        }
        catch (TimeoutException ex)
        {
            Console.WriteLine(ex.Message);
        }
    }
}
