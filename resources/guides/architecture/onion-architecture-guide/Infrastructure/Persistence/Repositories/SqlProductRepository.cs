using OnionArchitecture.Domain.Interfaces;
using OnionArchitecture.Domain.ValueObjects;

namespace OnionArchitecture.Infrastructure.Persistence.Repositories;

public class SqlProductRepository : IProductRepository
{
    private static readonly Product[] Seed =
    {
        new(Guid.Parse("00000000-0000-0000-0000-000000000001"), "Widget", new Money(9.99m)),
        new(Guid.Parse("00000000-0000-0000-0000-000000000002"), "Gadget", new Money(19.99m)),
        new(Guid.Parse("00000000-0000-0000-0000-000000000003"), "Sprocket", new Money(4.50m)),
    };

    public Task<Product?> GetByIdAsync(Guid id, CancellationToken ct = default) =>
        Task.FromResult(Seed.FirstOrDefault(p => p.Id == id));
}
