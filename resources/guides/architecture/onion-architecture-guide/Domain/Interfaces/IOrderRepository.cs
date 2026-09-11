using OnionArchitecture.Domain.Entities;

namespace OnionArchitecture.Domain.Interfaces;

public interface IOrderRepository
{
    Task<Order?> GetByIdAsync(Guid id, CancellationToken ct = default);
    Task SaveAsync(Order order, CancellationToken ct = default);
}
