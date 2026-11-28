using System.Threading.Tasks;

/// <summary>
/// Bounded-concurrency worker pool using SemaphoreSlim + Task.WhenAll.
/// </summary>
public class WorkerPool
{
    private readonly SemaphoreSlim _semaphore;

    public WorkerPool(int maxConcurrency)
    {
        _semaphore = new SemaphoreSlim(maxConcurrency);
    }

    public async Task<string[]> ProcessBatchAsync(IEnumerable<string> items)
    {
        var tasks = items.Select(async item =>
        {
            await _semaphore.WaitAsync();
            try
            {
                return await ProcessItemAsync(item);
            }
            finally
            {
                _semaphore.Release();
            }
        });

        return await Task.WhenAll(tasks);
    }

    private async Task<string> ProcessItemAsync(string item)
    {
        await Task.Delay(100); // simulate work
        return $"Processed: {item}";
    }
}
