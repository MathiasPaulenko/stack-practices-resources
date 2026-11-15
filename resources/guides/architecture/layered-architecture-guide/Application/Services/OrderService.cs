using ECommerce.Application.Dtos;
using ECommerce.Application.Exceptions;
using ECommerce.Application.Interfaces;
using ECommerce.Domain.Entities;
using ECommerce.Domain.Interfaces;

namespace ECommerce.Application.Services;

// Orchestration only: check stock -> create order -> persist -> return DTO.
// No HttpContext, no DbContext — this layer is unit-testable with mocks.
public class OrderService : IOrderService
{
    private readonly IOrderRepository _orderRepository;
    private readonly IProductRepository _productRepository;

    public OrderService(IOrderRepository orderRepository, IProductRepository productRepository)
    {
        _orderRepository = orderRepository;
        _productRepository = productRepository;
    }

    public async Task<OrderDto> CreateOrderAsync(int productId, int quantity)
    {
        var product = await _productRepository.GetByIdAsync(productId)
            ?? throw new BusinessException("Product not found.");

        if (!product.HasStockFor(quantity))
            throw new BusinessException("Insufficient stock.");

        var order = Order.Create(productId, quantity, product.Price);
        product.DecreaseStock(quantity);

        await _productRepository.UpdateAsync(product);
        await _orderRepository.AddAsync(order);

        return ToDto(order);
    }

    public async Task<OrderDto?> GetOrderAsync(int id)
    {
        var order = await _orderRepository.GetByIdAsync(id);
        return order is null ? null : ToDto(order);
    }

    private static OrderDto ToDto(Order order) =>
        new(order.Id, order.ProductId, order.Quantity, order.Total,
            order.Status.ToString(), order.CreatedAt);
}
