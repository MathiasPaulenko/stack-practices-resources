namespace OnionArchitecture.Domain.Events;

public record OrderPlacedEvent(Guid OrderId, decimal Total, string Currency, DateTime PlacedAt);
