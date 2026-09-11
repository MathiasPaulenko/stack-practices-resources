using OnionArchitecture.Domain.Events;
using OnionArchitecture.Domain.Exceptions;
using OnionArchitecture.Domain.ValueObjects;

namespace OnionArchitecture.Domain.Entities;

public class Order
{
    public OrderId Id { get; private set; }
    public Money Total { get; private set; }
    public DateTime CreatedAt { get; private set; }
    private readonly List<OrderLine> _lines = new();
    public IReadOnlyList<OrderLine> Lines => _lines.AsReadOnly();

    public Order() : this(OrderId.New()) { }

    public Order(OrderId id)
    {
        Id = id;
        Total = Money.Zero();
        CreatedAt = DateTime.UtcNow;
    }

    public void AddLine(Guid productId, string productName, Money unitPrice, int quantity)
    {
        if (quantity <= 0)
            throw new DomainException("Quantity must be positive");
        if (unitPrice < Money.Zero())
            throw new DomainException("Unit price cannot be negative");

        _lines.Add(new OrderLine(productId, productName, unitPrice, quantity));
        RecalculateTotal();
    }

    private void RecalculateTotal()
    {
        Total = _lines.Aggregate(Money.Zero(), (sum, line) => sum + line.Subtotal);
    }

    public OrderPlacedEvent Confirm()
    {
        if (_lines.Count == 0)
            throw new DomainException("Cannot confirm an empty order");
        return new OrderPlacedEvent(Id.Value, Total.Amount, Total.Currency, DateTime.UtcNow);
    }
}

public record OrderLine(Guid ProductId, string ProductName, Money UnitPrice, int Quantity)
{
    public Money Subtotal => new(UnitPrice.Amount * Quantity, UnitPrice.Currency);
}
