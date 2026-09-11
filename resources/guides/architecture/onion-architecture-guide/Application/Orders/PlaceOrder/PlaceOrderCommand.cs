namespace OnionArchitecture.Application.Orders.PlaceOrder;

public record PlaceOrderCommand(IEnumerable<OrderItem> Items);

public record OrderItem(Guid ProductId, int Quantity);
