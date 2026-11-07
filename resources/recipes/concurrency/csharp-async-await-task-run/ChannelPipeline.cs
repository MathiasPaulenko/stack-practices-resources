// Producer-consumer pipeline with a bounded channel (backpressure built in).
// Build: dotnet run ChannelPipeline.cs  — requires .NET 8+

using System.Threading.Channels;

public static class ChannelPipeline
{
    public static async Task RunAsync()
    {
        // Bounded channel: WriteAsync suspends when full — free backpressure.
        var channel = Channel.CreateBounded<int>(10);

        async Task ProduceAsync()
        {
            for (int i = 0; i < 100; i++)
            {
                await channel.Writer.WriteAsync(i);
            }
            // Without Complete() the readers wait forever for items that never come.
            channel.Writer.Complete();
        }

        async Task ConsumeAsync(int workerId)
        {
            await foreach (var item in channel.Reader.ReadAllAsync())
            {
                await Task.Delay(50); // Simulate work
            }
        }

        var consumers = Enumerable.Range(0, 3).Select(ConsumeAsync);
        var producer = ProduceAsync();

        await Task.WhenAll(Task.WhenAll(consumers), producer);
        Console.WriteLine("Channel processing complete");
    }

    public static async Task Main() => await RunAsync();
}
