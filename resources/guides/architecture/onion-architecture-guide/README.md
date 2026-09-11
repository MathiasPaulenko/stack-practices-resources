# Onion Architecture Guide — Companion Resources

This companion contains a complete C# implementation of the Onion Architecture
pattern described in the [Onion Architecture Guide](https://stackpractices.com/guides/onion-architecture-guide/).

## Structure

```
Domain/           # Domain Core — no external dependencies
  Entities/       # Order entity with business rules
  ValueObjects/   # Money, OrderId
  Events/         # OrderPlacedEvent
  Interfaces/     # IOrderRepository, IProductRepository, IEventBus (ports)
  Exceptions/     # DomainException
Application/      # Application Services — orchestrates use cases
  Orders/         # PlaceOrderCommand, PlaceOrderHandler
  Interfaces/     # IUnitOfWork
Infrastructure/   # Infrastructure — implements domain interfaces (adapters)
  Persistence/    # AppDbContext, SqlOrderRepository, SqlProductRepository
  Messaging/      # InMemoryEventBus
Presentation/     # Presentation — controllers
  Controllers/    # OrdersController
Tests/            # Unit tests for each layer
  DomainTests.cs          # 11 tests
  ApplicationTests.cs     # 6 tests
  ArchitectureTests.cs     # 6 tests
```

## Dependency Rule

All dependencies point inward:
- Domain depends on nothing (no EF Core, no ASP.NET).
- Application depends on Domain only.
- Infrastructure depends on Domain and Application (implements interfaces).
- Presentation depends on Application only.

## Running Tests

```bash
dotnet test
```

## Key Design Decisions

- **Value Objects**: `Money` and `OrderId` are `readonly struct` — immutable and
  validated at construction.
- **Domain Events**: `OrderPlacedEvent` is a `record` — immutable and structural
  equality.
- **Ports**: `IOrderRepository`, `IProductRepository`, `IEventBus` live in Domain.
- **Adapters**: `SqlOrderRepository`, `InMemoryEventBus` live in Infrastructure.
- **Architecture Tests**: Enforce dependency direction at compile time.

## Source

- [English guide](https://stackpractices.com/guides/onion-architecture-guide/)
- [Spanish guide](https://stackpractices.com/es/guides/onion-architecture-guide/)
