using Moq;
using OnionArchitecture.Application.Interfaces;
using OnionArchitecture.Application.Orders.PlaceOrder;
using OnionArchitecture.Domain.Entities;
using OnionArchitecture.Domain.Exceptions;
using OnionArchitecture.Domain.Interfaces;
using OnionArchitecture.Domain.ValueObjects;
using OnionArchitecture.Infrastructure.Messaging;
using Xunit;

namespace OnionArchitecture.Tests;

public class ApplicationTests
{
    private readonly Mock<IOrderRepository> _orderRepo = new();
    private readonly Mock<IProductRepository> _productRepo = new();
    private readonly Mock<IUnitOfWork> _unitOfWork = new();
    private readonly InMemoryEventBus _eventBus = new();

    private PlaceOrderHandler CreateHandler() => new(
        _orderRepo.Object, _productRepo.Object, _eventBus, _unitOfWork.Object);

    [Fact]
    public async Task Handle_ValidCommand_ReturnsOrderId()
    {
        var productId = Guid.Parse("00000000-0000-0000-0000-000000000001");
        _productRepo.Setup(r => r.GetByIdAsync(productId, It.IsAny<CancellationToken>()))
            .ReturnsAsync(new Product(productId, "Widget", new Money(9.99m)));
        var handler = CreateHandler();
        var command = new PlaceOrderCommand(new[] { new OrderItem(productId, 2) });

        var orderId = await handler.Handle(command);

        Assert.NotEqual(Guid.Empty, orderId);
        _orderRepo.Verify(r => r.SaveAsync(It.IsAny<Order>(), It.IsAny<CancellationToken>()), Times.Once);
        _unitOfWork.Verify(u => u.SaveChangesAsync(It.IsAny<CancellationToken>()), Times.Once);
        Assert.Single(_eventBus.PublishedEvents);
    }

    [Fact]
    public async Task Handle_UnknownProduct_ThrowsDomainException()
    {
        _productRepo.Setup(r => r.GetByIdAsync(It.IsAny<Guid>(), It.IsAny<CancellationToken>()))
            .ReturnsAsync((Product?)null);
        var handler = CreateHandler();
        var command = new PlaceOrderCommand(new[] { new OrderItem(Guid.NewGuid(), 1) });

        await Assert.ThrowsAsync<DomainException>(() => handler.Handle(command));
    }

    [Fact]
    public async Task Handle_ZeroQuantity_ThrowsDomainException()
    {
        var productId = Guid.NewGuid();
        _productRepo.Setup(r => r.GetByIdAsync(productId, It.IsAny<CancellationToken>()))
            .ReturnsAsync(new Product(productId, "Widget", new Money(5m)));
        var handler = CreateHandler();
        var command = new PlaceOrderCommand(new[] { new OrderItem(productId, 0) });

        await Assert.ThrowsAsync<DomainException>(() => handler.Handle(command));
    }

    [Fact]
    public async Task Handle_NullCommand_ThrowsDomainException()
    {
        var handler = CreateHandler();
        await Assert.ThrowsAsync<DomainException>(() => handler.Handle(null!));
    }

    [Fact]
    public async Task Handle_PublishesOrderPlacedEvent()
    {
        var productId = Guid.Parse("00000000-0000-0000-0000-000000000002");
        _productRepo.Setup(r => r.GetByIdAsync(productId, It.IsAny<CancellationToken>()))
            .ReturnsAsync(new Product(productId, "Gadget", new Money(19.99m)));
        var handler = CreateHandler();
        var command = new PlaceOrderCommand(new[] { new OrderItem(productId, 3) });

        await handler.Handle(command);

        Assert.Single(_eventBus.PublishedEvents);
        Assert.IsType<OrderPlacedEvent>(_eventBus.PublishedEvents[0]);
    }

    [Fact]
    public async Task Handle_MultipleItems_CalculatesTotalCorrectly()
    {
        var p1 = Guid.Parse("00000000-0000-0000-0000-000000000001");
        var p2 = Guid.Parse("00000000-0000-0000-0000-000000000003");
        _productRepo.Setup(r => r.GetByIdAsync(p1, It.IsAny<CancellationToken>()))
            .ReturnsAsync(new Product(p1, "Widget", new Money(9.99m)));
        _productRepo.Setup(r => r.GetByIdAsync(p2, It.IsAny<CancellationToken>()))
            .ReturnsAsync(new Product(p2, "Sprocket", new Money(4.50m)));
        var handler = CreateHandler();
        var command = new PlaceOrderCommand(new[]
        {
            new OrderItem(p1, 2),
            new OrderItem(p2, 4),
        });

        var orderId = await handler.Handle(command);

        Assert.NotEqual(Guid.Empty, orderId);
        var evt = Assert.IsType<OrderPlacedEvent>(_eventBus.PublishedEvents[0]);
        Assert.Equal(9.99m * 2 + 4.50m * 4, evt.Total);
    }
}
