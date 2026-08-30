// Customer.Custom.cs — hand-written business logic
public partial class Customer
{
    public bool IsValidEmail()
    {
        return Email?.Contains("@") ?? false;
    }

    public string GetDisplayName()
    {
        return $"{Name} <{Email}>";
    }
}
