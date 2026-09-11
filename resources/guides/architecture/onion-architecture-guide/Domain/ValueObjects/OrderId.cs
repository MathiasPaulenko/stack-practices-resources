namespace OnionArchitecture.Domain.ValueObjects;

public readonly struct OrderId : IEquatable<OrderId>
{
    public Guid Value { get; }

    public OrderId(Guid value)
    {
        if (value == Guid.Empty)
            throw new ArgumentException("OrderId cannot be empty", nameof(value));
        Value = value;
    }

    public static OrderId New() => new(Guid.NewGuid());

    public bool Equals(OrderId other) => Value == other.Value;
    public override bool Equals(object? obj) => obj is OrderId other && Equals(other);
    public override int GetHashCode() => Value.GetHashCode();
    public override string ToString() => Value.ToString();

    public static bool operator ==(OrderId left, OrderId right) => left.Equals(right);
    public static bool operator !=(OrderId left, OrderId right) => !left.Equals(right);
}
