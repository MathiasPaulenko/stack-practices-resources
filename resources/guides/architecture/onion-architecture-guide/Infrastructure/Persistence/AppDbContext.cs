using Microsoft.EntityFrameworkCore;
using OnionArchitecture.Domain.Entities;

namespace OnionArchitecture.Infrastructure.Persistence;

public class AppDbContext : DbContext
{
    public AppDbContext(DbContextOptions<AppDbContext> options) : base(options) { }

    public DbSet<Order> Orders => Set<Order>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<Order>(entity =>
        {
            entity.HasKey(o => o.Id);
            entity.Property(o => o.CreatedAt).IsRequired();
            entity.Ignore(o => o.Total);
            entity.Ignore(o => o.Lines);
        });
    }
}
