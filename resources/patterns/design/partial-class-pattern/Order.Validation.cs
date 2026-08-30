// Order.Validation.cs
using System.Collections.Generic;

public partial class Order
{
    public bool IsValid()
    {
        return Items.Count > 0 && Total > 0
            && !string.IsNullOrEmpty(CustomerEmail);
    }

    public List<string> GetValidationErrors()
    {
        var errors = new List<string>();
        if (Items.Count == 0) errors.Add("Order must have items");
        if (Total <= 0) errors.Add("Total must be positive");
        if (string.IsNullOrEmpty(CustomerEmail))
            errors.Add("Email required");
        return errors;
    }
}
