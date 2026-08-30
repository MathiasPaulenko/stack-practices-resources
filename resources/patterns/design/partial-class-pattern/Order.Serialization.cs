// Order.Serialization.cs
using System;
using System.Text.Json;

public partial class Order
{
    public string ToJson()
    {
        return JsonSerializer.Serialize(this);
    }

    public static Order FromJson(string json)
    {
        return JsonSerializer.Deserialize<Order>(json)
            ?? throw new InvalidOperationException("Invalid JSON");
    }
}
