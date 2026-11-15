using ECommerce.Application.Dtos;

namespace ECommerce.Application.Interfaces;

// The contract Presentation calls. Application owns orchestration;
// the domain owns the rules.
public interface IOrderService
{
    Task<OrderDto> CreateOrderAsync(int productId, int quantity);
    Task<OrderDto?> GetOrderAsync(int id);
}
