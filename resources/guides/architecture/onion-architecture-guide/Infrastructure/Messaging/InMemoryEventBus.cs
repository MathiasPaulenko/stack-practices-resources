using OnionArchitecture.Domain.Interfaces;

namespace OnionArchitecture.Infrastructure.Messaging;

public class InMemoryEventBus : IEventBus
{
    private readonly List<object> _published = new();
    public IReadOnlyList<object> PublishedEvents => _published.AsReadOnly();

    public Task PublishAsync<T>(T @event, CancellationToken ct = default) where T : notnull
    {
        _published.Add(@event);
        return Task.CompletedTask;
    }

    public void Clear() => _published.Clear();
}
