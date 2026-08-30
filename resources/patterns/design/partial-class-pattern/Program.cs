using System;
using System.Collections.Generic;

class Program
{
    static void Main()
    {
        var customer = new Customer
        {
            Id = 1,
            Name = "Alice",
            Email = "alice@example.com"
        };

        Console.WriteLine($"Email valid: {customer.IsValidEmail()}");
        Console.WriteLine(customer.GetDisplayName());

        var order = new Order
        {
            Id = Guid.NewGuid(),
            CustomerEmail = customer.Email,
            Items = new List<OrderItem>
            {
                new OrderItem { Name = "Book", Price = 20m, Quantity = 2 }
            },
            Total = 40m,
            CreatedAt = DateTime.UtcNow
        };

        Console.WriteLine($"Order valid: {order.IsValid()}");

        order.ApplyDiscount(10);
        Console.WriteLine($"After 10% discount: {order.Total}");

        order.ApplyCoupon("SAVE10");
        Console.WriteLine($"After SAVE10 coupon: {order.Total}");

        var json = order.ToJson();
        Console.WriteLine($"JSON: {json}");

        var roundTrip = Order.FromJson(json);
        Console.WriteLine($"Round-trip email: {roundTrip.CustomerEmail}");
    }
}
