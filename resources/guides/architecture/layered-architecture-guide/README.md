# Layered Architecture — Companion C# Solution Layout

A runnable .NET-style project layout matching the four-layer e-commerce example from the [Layered Architecture guide](https://stackpractices.com/guides/layered-architecture-guide/) on StackPractices.

## Structure

```
Presentation/   -> Controllers (thin) + Program.cs DI wiring
Application/    -> OrderService orchestration, DTOs, BusinessException
Domain/         -> Order/Product entities with real rules, repository interfaces
Infrastructure/ -> EF Core AppDbContext + repository implementations
Tests/          -> xUnit + Moq unit tests (mock the layer below)
```

## Dependency rules enforced by the layout

```
Web -> Application -> Domain
Infrastructure -> Domain   (fulfills domain interfaces)
Domain depends on nothing  (zero external references)
```

## Contents

| File | Purpose |
|------|---------|
| `Domain/Entities/Order.cs` | Entity with real rules: `Create` validates quantity/price, `Cancel` rejects shipped orders |
| `Domain/Entities/Product.cs` | Stock invariant lives on the entity (`DecreaseStock`) |
| `Domain/Interfaces/*.cs` | `IOrderRepository`, `IProductRepository` — owned by the domain |
| `Application/Services/OrderService.cs` | Orchestration: check stock → create order → persist → DTO |
| `Application/Dtos/OrderDto.cs` | One DTO at the API boundary; entities never serialize out |
| `Application/Exceptions/BusinessException.cs` | Rule violations map to 422 at the controller edge |
| `Infrastructure/Persistence/*` | `AppDbContext` + EF Core repositories fulfilling domain interfaces |
| `Presentation/Controllers/OrderController.cs` | Thin controller: HTTP in/out only |
| `Presentation/Program.cs` | DI wiring — where the layers get connected |
| `Tests/OrderServiceTests.cs` | Application tests mock repositories; no database needed |

## Notes

- Application tests never touch a database — they fake `IOrderRepository`/`IProductRepository`. Repository tests belong in integration tests against a real database (e.g. Testcontainers).
- `Order.Create` is a factory that enforces invariants, so no caller can produce an invalid order — the fix for an anemic domain model.
- Copy each folder into a same-named .csproj (`ECommerce.Web`, `ECommerce.Application`, `ECommerce.Domain`, `ECommerce.Infrastructure`) to make dependency violations compile errors.
