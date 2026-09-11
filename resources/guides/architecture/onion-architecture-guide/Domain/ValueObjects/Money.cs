namespace OnionArchitecture.Domain.ValueObjects;

public readonly struct Money : IEquatable<Money>, IComparable<Money>
{
    public decimal Amount { get; }
    public string Currency { get; }

    public Money(decimal amount, string currency = "USD")
    {
        if (amount < 0)
            throw new ArgumentException("Money amount cannot be negative", nameof(amount));
        if (string.IsNullOrWhiteSpace(currency))
            throw new ArgumentException("Currency is required", nameof(currency));
        Amount = amount;
        Currency = currency;
    }

    public static Money Zero(string currency = "USD") => new(0, currency);

    public static Money operator +(Money left, Money right)
    {
        if (left.Currency != right.Currency)
            throw new InvalidOperationException("Cannot add money with different currencies");
        return new Money(left.Amount + right.Amount, left.Currency);
    }

    public static bool operator >(Money left, Money right) =>
        left.Currency == right.Currency && left.Amount > right.Amount;
    public static bool operator <(Money left, Money right) =>
        left.Currency == right.Currency && left.Amount < right.Amount;

    public bool Equals(Money other) => Amount == other.Amount && Currency == other.Currency;
    public override bool Equals(object? obj) => obj is Money other && Equals(other);
    public override int GetHashCode() => HashCode.Combine(Amount, Currency);
    public int CompareTo(Money other) => Amount.CompareTo(other.Amount);
    public override string ToString() => $"{Amount:F2} {Currency}";
}
