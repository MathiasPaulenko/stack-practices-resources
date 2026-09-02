// Program.cs
using Carter;
using FluentValidation;
using MediatR;
using Microsoft.EntityFrameworkCore;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseInMemoryDatabase("VerticalSliceDemo"));

builder.Services.AddMediatR(cfg => cfg.RegisterServicesFromAssemblyContaining<Program>());
builder.Services.AddValidatorsFromAssemblyContaining<Program>();
builder.Services.AddTransient(typeof(IPipelineBehavior<,>), typeof(LoggingBehavior<,>));
builder.Services.AddTransient(typeof(IPipelineBehavior<,>), typeof(ValidationBehavior<,>));
builder.Services.AddCarter();

var app = builder.Build();

app.MapCarter();

// Seed data
using (var scope = app.Services.CreateScope())
{
    var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();
    db.Products.Add(new Product { Id = 1, Name = "Widget", Price = 10m, Stock = 100 });
    db.Products.Add(new Product { Id = 2, Name = "Gadget", Price = 25m, Stock = 50 });
    await db.SaveChangesAsync();
}

app.Run();
