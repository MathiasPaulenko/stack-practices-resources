using ECommerce.Domain.Entities;
using ECommerce.Domain.Interfaces;
using Microsoft.EntityFrameworkCore;

namespace ECommerce.Infrastructure.Persistence.Repositories;

// Infrastructure fulfills the domain contract. Web and Application
// never see this class — only the IOrderRepository interface.
public class OrderRepository : IOrderRepository
{
    private readonly AppDbContext _context;

    public OrderRepository(AppDbContext context) => _context = context;

    public async Task<Order?> GetByIdAsync(int id) =>
        await _context.Orders.FindAsync(id);

    public async Task AddAsync(Order order)
    {
        _context.Orders.Add(order);
        await _context.SaveChangesAsync();
    }

    public async Task<IReadOnlyList<Order>> GetPendingAsync() =>
        await _context.Orders
            .AsNoTracking()
            .Where(o => o.Status == OrderStatus.Pending)
            .ToListAsync();
}
