namespace ECommerce.Application.Dtos;

// One DTO at the API boundary — the entity never leaks to the response.
public record OrderDto(
    int Id,
    int ProductId,
    int Quantity,
    decimal Total,
    string Status,
    DateTime CreatedAt);
