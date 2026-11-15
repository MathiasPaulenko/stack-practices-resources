namespace ECommerce.Domain.Entities;

public enum OrderStatus
{
    Pending,
    Confirmed,
    Shipped,
    Cancelled
}

public class Order
{
    private const int MaxItems = 100;

    public int Id { get; private set; }
    public int ProductId { get; private set; }
    public int Quantity { get; private set; }
    public decimal Total { get; private set; }
    public OrderStatus Status { get; private set; }
    public DateTime CreatedAt { get; private set; }

    private Order() { }

    // Business rules live in the domain, not in the service:
    // min 1 item, max 100, total must be positive.
    public static Order Create(int productId, int quantity, decimal unitPrice)
    {
        if (quantity < 1 || quantity > MaxItems)
            throw new InvalidOperationException($"Quantity must be between 1 and {MaxItems}.");
        if (unitPrice <= 0)
            throw new InvalidOperationException("Price must be positive.");

        return new Order
        {
            ProductId = productId,
            Quantity = quantity,
            Total = unitPrice * quantity,
            Status = OrderStatus.Pending,
            CreatedAt = DateTime.UtcNow
        };
    }

    // A shipped order cannot be cancelled — the entity enforces it.
    public void Cancel()
    {
        if (Status == OrderStatus.Shipped)
            throw new InvalidOperationException("Cannot cancel a shipped order.");
        Status = OrderStatus.Cancelled;
    }

    public void Confirm() => Status = OrderStatus.Confirmed;
}
