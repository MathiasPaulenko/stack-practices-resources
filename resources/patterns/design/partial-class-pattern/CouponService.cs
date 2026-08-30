public static class CouponService
{
    public static (bool IsValid, decimal Amount) Validate(string code)
    {
        if (code == "SAVE10") return (true, 10m);
        return (false, 0m);
    }
}
