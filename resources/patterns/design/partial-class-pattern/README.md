# Partial Class Pattern — C\# Companion

Runnable companion files for the StackPractices pattern
[Partial Class Pattern](https://stackpractices.com/patterns/partial-class-pattern/).

## Requirements

- .NET 8 SDK or later

## Quick start

```bash
# Build and run
dotnet run

# Or build only
dotnet build
```

## Files

- `Customer.generated.cs` — scaffolded properties (`Id`, `Name`, `Email`).
- `Customer.custom.cs` — hand-written validation and display logic.
- `Order.cs` — main order model.
- `Order.Validation.cs` — validation rules.
- `Order.Pricing.cs` — discounts, coupons and tax.
- `Order.Serialization.cs` — JSON serialization helpers.
- `OrderItem.cs` — order line item.
- `CouponService.cs` — simple coupon validation stub.
- `Program.cs` — demo usage.

The compiler merges every `partial class Order` file into a single `Order` type.
Edit only the `*.custom.cs` files if the model is regenerated from a database or
other source.
