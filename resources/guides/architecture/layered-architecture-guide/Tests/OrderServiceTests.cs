using ECommerce.Application.Exceptions;
using ECommerce.Application.Services;
using ECommerce.Domain.Entities;
using ECommerce.Domain.Interfaces;
using Moq;
using Xunit;

namespace ECommerce.Tests;

// Application layer tests: mock the layer below (repositories), never
// touch a real database. Repository tests belong in integration tests
// with Testcontainers instead.
public class OrderServiceTests
{
    private readonly Mock<IOrderRepository> _orders = new();
    private readonly Mock<IProductRepository> _products = new();

    private OrderService CreateService() =>
        new(_orders.Object, _products.Object);

    [Fact]
    public async Task CreateOrderAsync_InsufficientStock_Throws()
    {
        _products.Setup(r => r.GetByIdAsync(1))
            .ReturnsAsync(new Product { Id = 1, Name = "Widget", Price = 10m });
        // Stock = 0 by default; requesting 5 must fail before persist.
        var service = CreateService();

        await Assert.ThrowsAsync<BusinessException>(
            () => service.CreateOrderAsync(productId: 1, quantity: 5));

        _orders.Verify(r => r.AddAsync(It.IsAny<Order>()), Times.Never);
    }

    [Fact]
    public async Task CreateOrderAsync_ValidRequest_PersistsOrder()
    {
        var product = new Product { Id = 1, Name = "Widget", Price = 10m };
        typeof(Product).GetProperty(nameof(Product.Stock))!
            .SetValue(product, 20); // seed stock for the test

        _products.Setup(r => r.GetByIdAsync(1)).ReturnsAsync(product);
        var service = CreateService();

        var dto = await service.CreateOrderAsync(productId: 1, quantity: 3);

        Assert.Equal(30m, dto.Total);
        Assert.Equal("Pending", dto.Status);
        _orders.Verify(r => r.AddAsync(It.IsAny<Order>()), Times.Once);
        _products.Verify(r => r.UpdateAsync(product), Times.Once);
    }

    [Fact]
    public async Task CreateOrderAsync_UnknownProduct_Throws()
    {
        _products.Setup(r => r.GetByIdAsync(It.IsAny<int>()))
            .ReturnsAsync((Product?)null);
        var service = CreateService();

        await Assert.ThrowsAsync<BusinessException>(
            () => service.CreateOrderAsync(productId: 999, quantity: 1));
    }
}
