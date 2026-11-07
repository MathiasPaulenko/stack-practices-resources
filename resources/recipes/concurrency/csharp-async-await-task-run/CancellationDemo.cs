// Cooperative cancellation with CancellationTokenSource.
// Build: dotnet run CancellationDemo.cs — requires .NET 8+

public static class CancellationDemo
{
    public static async Task ProcessAsync(CancellationToken ct)
    {
        for (int i = 0; i < 100; i++)
        {
            // Cooperative: check the token and pass it to calls that honor it.
            ct.ThrowIfCancellationRequested();
            await Task.Delay(100, ct);
            Console.WriteLine($"Processing item {i}");
        }
    }

    public static async Task Main()
    {
        using var cts = new CancellationTokenSource();
        cts.CancelAfter(TimeSpan.FromMilliseconds(500));

        try
        {
            await ProcessAsync(cts.Token);
        }
        catch (OperationCanceledException)
        {
            Console.WriteLine("Operation was cancelled — cleaned up politely");
        }
    }
}
