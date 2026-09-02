// Features/Orders/CreateOrder/CreateOrderCommand.cs
using MediatR;

public record CreateOrderCommand(
    int ProductId,
    int Quantity,
    string CustomerEmail
) : IRequest<OrderDto>;

public record OrderDto(int Id, int ProductId, int Quantity, string CustomerEmail, decimal Total, DateTime CreatedAt);
