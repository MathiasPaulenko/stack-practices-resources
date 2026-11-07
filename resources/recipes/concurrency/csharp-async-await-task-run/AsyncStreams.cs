// IAsyncEnumerable — streaming results as they become available.
// Build: dotnet run AsyncStreams.cs — requires .NET 8+

using System.Runtime.CompilerServices;

public static class AsyncStreams
{
    public static async IAsyncEnumerable<int> GenerateAsync(
        int count,
        [EnumeratorCancellation] CancellationToken ct = default)
    {
        for (int i = 0; i < count; i++)
        {
            ct.ThrowIfCancellationRequested();
            await Task.Delay(50, ct);
            yield return i; // Consumer sees each value as it's produced
        }
    }

    public static async Task Main()
    {
        using var cts = new CancellationTokenSource(TimeSpan.FromMilliseconds(400));

        try
        {
            await foreach (var num in GenerateAsync(100, cts.Token))
            {
                Console.WriteLine($"Received: {num}");
            }
        }
        catch (OperationCanceledException)
        {
            Console.WriteLine("Stream cancelled");
        }
    }
}
