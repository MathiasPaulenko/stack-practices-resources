namespace ECommerce.Domain.Entities;

public class Product
{
    public int Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public decimal Price { get; set; }
    public int Stock { get; private set; }

    public bool HasStockFor(int quantity) => Stock >= quantity;

    public void DecreaseStock(int quantity)
    {
        if (!HasStockFor(quantity))
            throw new InvalidOperationException("Insufficient stock.");
        Stock -= quantity;
    }
}
