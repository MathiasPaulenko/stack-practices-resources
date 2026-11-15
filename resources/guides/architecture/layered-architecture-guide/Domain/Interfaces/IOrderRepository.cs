using ECommerce.Domain.Entities;

namespace ECommerce.Domain.Interfaces;

// Defined by the domain, fulfilled by Infrastructure.
// The domain never references EF Core or any ORM.
public interface IOrderRepository
{
    Task<Order?> GetByIdAsync(int id);
    Task AddAsync(Order order);
    Task<IReadOnlyList<Order>> GetPendingAsync();
}
