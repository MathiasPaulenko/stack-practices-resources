# Guía de Arquitectura Onion — Recursos Companion

Este companion contiene una implementación completa en C# del patrón de
Arquitectura Onion descrito en la [Guía de Arquitectura Onion](https://stackpractices.com/es/guides/onion-architecture-guide/).

## Estructura

```
Domain/           # Núcleo de Dominio — sin dependencias externas
  Entities/       # Entidad Order con reglas de negocio
  ValueObjects/   # Money, OrderId
  Events/         # OrderPlacedEvent
  Interfaces/     # IOrderRepository, IProductRepository, IEventBus (puertos)
  Exceptions/     # DomainException
Application/      # Servicios de Aplicación — orquesta casos de uso
  Orders/         # PlaceOrderCommand, PlaceOrderHandler
  Interfaces/     # IUnitOfWork
Infrastructure/   # Infraestructura — implementa interfaces del dominio (adaptadores)
  Persistence/    # AppDbContext, SqlOrderRepository, SqlProductRepository
  Messaging/      # InMemoryEventBus
Presentation/     # Presentación — controladores
  Controllers/    # OrdersController
Tests/            # Tests unitarios para cada capa
  DomainTests.cs          # 11 tests
  ApplicationTests.cs     # 6 tests
  ArchitectureTests.cs     # 6 tests
```

## Regla de Dependencia

Todas las dependencias apuntan hacia adentro:
- Domain no depende de nada (sin EF Core, sin ASP.NET).
- Application depende solo de Domain.
- Infrastructure depende de Domain y Application (implementa interfaces).
- Presentation depende solo de Application.

## Ejecutar Tests

```bash
dotnet test
```

## Decisiones de Diseño Clave

- **Value Objects**: `Money` y `OrderId` son `readonly struct` — inmutables y
  validados al construirse.
- **Eventos de Dominio**: `OrderPlacedEvent` es un `record` — inmutable con
  igualdad estructural.
- **Puertos**: `IOrderRepository`, `IProductRepository`, `IEventBus` viven en Domain.
- **Adaptadores**: `SqlOrderRepository`, `InMemoryEventBus` viven en Infrastructure.
- **Tests de Arquitectura**: Forzan la dirección de dependencias en tiempo de
  compilación.

## Fuente

- [Guía en inglés](https://stackpractices.com/guides/onion-architecture-guide/)
- [Guía en español](https://stackpractices.com/es/guides/onion-architecture-guide/)
