using Microsoft.EntityFrameworkCore;
using OnionArchitecture.Domain.Entities;
using OnionArchitecture.Domain.Interfaces;

namespace OnionArchitecture.Infrastructure.Persistence.Repositories;

public class SqlOrderRepository : IOrderRepository
{
    private readonly AppDbContext _dbContext;

    public SqlOrderRepository(AppDbContext dbContext) => _dbContext = dbContext;

    public Task<Order?> GetByIdAsync(Guid id, CancellationToken ct = default) =>
        _dbContext.Orders.FirstOrDefaultAsync(o => o.Id.Value == id, ct);

    public async Task SaveAsync(Order order, CancellationToken ct = default)
    {
        var existing = await _dbContext.Orders.FirstOrDefaultAsync(o => o.Id.Value == order.Id.Value, ct);
        if (existing is null)
            _dbContext.Orders.Add(order);
        await _dbContext.SaveChangesAsync(ct);
    }
}
