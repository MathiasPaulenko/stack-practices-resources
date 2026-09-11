using OnionArchitecture.Domain.ValueObjects;

namespace OnionArchitecture.Domain.Interfaces;

public interface IProductRepository
{
    Task<Product?> GetByIdAsync(Guid id, CancellationToken ct = default);
}

public record Product(Guid Id, string Name, Money Price);
