using OnionArchitecture.Domain.Entities;
using OnionArchitecture.Domain.Exceptions;
using OnionArchitecture.Domain.ValueObjects;
using Xunit;

namespace OnionArchitecture.Tests;

public class DomainTests
{
    [Fact]
    public void Order_AddLine_WithPositiveQuantity_UpdatesTotal()
    {
        var order = new Order();
        var price = new Money(10m);
        order.AddLine(Guid.NewGuid(), "Widget", price, 3);
        Assert.Equal(30m, order.Total.Amount);
        Assert.Single(order.Lines);
    }

    [Fact]
    public void Order_AddLine_WithZeroQuantity_ThrowsDomainException()
    {
        var order = new Order();
        var ex = Assert.Throws<DomainException>(() =>
            order.AddLine(Guid.NewGuid(), "Widget", new Money(10m), 0));
        Assert.Contains("positive", ex.Message);
    }

    [Fact]
    public void Order_AddLine_WithNegativePrice_ThrowsDomainException()
    {
        var order = new Order();
        Assert.Throws<DomainException>(() =>
            order.AddLine(Guid.NewGuid(), "Widget", new Money(-1m), 1));
    }

    [Fact]
    public void Order_Confirm_WithEmptyLines_ThrowsDomainException()
    {
        var order = new Order();
        Assert.Throws<DomainException>(() => order.Confirm());
    }

    [Fact]
    public void Order_Confirm_WithLines_ReturnsEventWithTotal()
    {
        var order = new Order();
        order.AddLine(Guid.NewGuid(), "Widget", new Money(15m), 2);
        var evt = order.Confirm();
        Assert.Equal(30m, evt.Total);
        Assert.Equal(order.Id.Value, evt.OrderId);
    }

    [Fact]
    public void Money_Add_SameCurrency_ReturnsSum()
    {
        var a = new Money(5m);
        var b = new Money(3m);
        Assert.Equal(8m, (a + b).Amount);
    }

    [Fact]
    public void Money_Add_DifferentCurrency_Throws()
    {
        var usd = new Money(5m, "USD");
        var eur = new Money(3m, "EUR");
        Assert.Throws<InvalidOperationException>(() => usd + eur);
    }

    [Fact]
    public void Money_NegativeAmount_Throws()
    {
        Assert.Throws<ArgumentException>(() => new Money(-5m));
    }

    [Fact]
    public void OrderId_EmptyGuid_Throws()
    {
        Assert.Throws<ArgumentException>(() => new OrderId(Guid.Empty));
    }

    [Fact]
    public void OrderId_New_ReturnsNonEmpty()
    {
        var id = OrderId.New();
        Assert.NotEqual(Guid.Empty, id.Value);
    }

    [Fact]
    public void OrderLine_Subtotal_CalculatesCorrectly()
    {
        var line = new OrderLine(Guid.NewGuid(), "Widget", new Money(12.50m), 4);
        Assert.Equal(50m, line.Subtotal.Amount);
    }
}
