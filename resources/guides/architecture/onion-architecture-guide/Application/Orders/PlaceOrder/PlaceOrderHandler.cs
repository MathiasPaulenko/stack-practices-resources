using OnionArchitecture.Application.Interfaces;
using OnionArchitecture.Domain.Entities;
using OnionArchitecture.Domain.Events;
using OnionArchitecture.Domain.Exceptions;
using OnionArchitecture.Domain.Interfaces;

namespace OnionArchitecture.Application.Orders.PlaceOrder;

public class PlaceOrderHandler
{
    private readonly IOrderRepository _orderRepository;
    private readonly IProductRepository _productRepository;
    private readonly IEventBus _eventBus;
    private readonly IUnitOfWork _unitOfWork;

    public PlaceOrderHandler(
        IOrderRepository orderRepository,
        IProductRepository productRepository,
        IEventBus eventBus,
        IUnitOfWork unitOfWork)
    {
        _orderRepository = orderRepository;
        _productRepository = productRepository;
        _eventBus = eventBus;
        _unitOfWork = unitOfWork;
    }

    public async Task<Guid> Handle(PlaceOrderCommand command, CancellationToken ct = default)
    {
        if (command is null || command.Items is null)
            throw new DomainException("Command cannot be null");

        var order = new Order();

        foreach (var item in command.Items)
        {
            var product = await _productRepository.GetByIdAsync(item.ProductId, ct);
            if (product is null)
                throw new DomainException($"Product {item.ProductId} not found");
            order.AddLine(product.Id, product.Name, product.Price, item.Quantity);
        }

        var evt = order.Confirm();
        await _orderRepository.SaveAsync(order, ct);
        await _unitOfWork.SaveChangesAsync(ct);
        await _eventBus.PublishAsync(evt, ct);

        return order.Id.Value;
    }
}
