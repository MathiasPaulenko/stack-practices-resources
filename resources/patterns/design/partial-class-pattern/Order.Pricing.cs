// Order.Pricing.cs
public partial class Order
{
    public void ApplyDiscount(decimal percentage)
    {
        Total = Total * (1 - percentage / 100);
    }

    public void ApplyCoupon(string code)
    {
        var coupon = CouponService.Validate(code);
        if (coupon.IsValid) Total -= coupon.Amount;
    }

    public decimal CalculateTax(decimal rate)
    {
        return Total * rate;
    }
}
