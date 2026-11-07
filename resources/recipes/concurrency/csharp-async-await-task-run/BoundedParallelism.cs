// Bounded parallelism two ways: Parallel.ForEachAsync and SemaphoreSlim.
// Build: dotnet run BoundedParallelism.cs — requires .NET 6+

public static class BoundedParallelism
{
    private static readonly HttpClient client = new();

    public static async Task ParallelForEachDemoAsync()
    {
        var urls = Enumerable.Range(1, 20)
            .Select(i => $"https://httpbin.org/delay/1?page={i}");

        var options = new ParallelOptions { MaxDegreeOfParallelism = 5 };
        int ok = 0;

        await Parallel.ForEachAsync(urls, options, async (url, ct) =>
        {
            try
            {
                await client.GetStringAsync(url, ct);
                Interlocked.Increment(ref ok);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Failed {url}: {ex.Message}");
            }
        });

        Console.WriteLine($"ForEachAsync: {ok}/20 succeeded");
    }

    public static async Task SemaphoreDemoAsync()
    {
        var urls = Enumerable.Range(1, 50)
            .Select(i => $"https://httpbin.org/delay/1?id={i}");

        using var gate = new SemaphoreSlim(5); // Max 5 concurrent

        var tasks = urls.Select(async url =>
        {
            await gate.WaitAsync();
            try
            {
                return (await client.GetStringAsync(url)).Length;
            }
            finally
            {
                gate.Release();
            }
        });

        var results = await Task.WhenAll(tasks);
        Console.WriteLine($"SemaphoreSlim: fetched {results.Length} URLs");
    }

    public static async Task Main()
    {
        await ParallelForEachDemoAsync();
        await SemaphoreDemoAsync();
    }
}
